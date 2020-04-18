import numpy as np

from functools import partial
from profilehooks import profile

import sys
import pickle
import _thread as thread

import sounddevice as sd
import soundfile as sf

import soundwave.algorithms.least_mean_squares as lmsalgos
import soundwave.playback.playback as player
import soundwave.microphone.microphone as mic
import soundwave.plotting.plot as plot

import soundwave.bluetoothnetwork.server as btserver
import soundwave.bluetoothnetwork.client as btclient

mu = 0.00001
targetLocation = 0
liveInputSignal = None
liveTargetSignal = None
liveOutputSignal = None
liveErrorSignal = None
processing = True

errorBuffer = np.arange(2).reshape(1,2)
outputBuffer = np.arange(2).reshape(1,2)
referenceBuffer = []

def run_algorithm(algorithm, inputSignal, targetSignal, numChannels):
    switcher = {
        'lms': partial(lmsalgos.lms, inputSignal, targetSignal, mu, numChannels),
        'nlms': partial(lmsalgos.nlms, inputSignal, targetSignal, mu, numChannels),
        'nsslms': partial(lmsalgos.nsslms, inputSignal, targetSignal, mu, numChannels),
        'rls': partial(lmsalgos.rls, inputSignal, targetSignal, mu, numChannels),
        'clms': partial(lmsalgos.clms, inputSignal, targetSignal, mu, numChannels),
        'crls': partial(lmsalgos.crls, inputSignal, targetSignal, mu, numChannels)
    }

    func = switcher.get(algorithm)
    return func()


def process_signal(inputSignal, targetSignal, algorithm):
    # loop over each channel and perform the algorithm
    numChannels = len(inputSignal[0])
    outputSignal = None
    errorSignal = None
    for channel in range(numChannels):
        targetChannel = targetSignal[:, channel]
        inputChannel = np.stack((inputSignal[:, channel],
                                 targetChannel), axis=1)

        # perform algorithm on left channel, then right right
        outputChannel, errorChannel = run_algorithm(
            algorithm, inputChannel, targetChannel, numChannels)

        if outputSignal is None:
            outputSignal = outputChannel
            errorSignal = errorChannel
        else:
            outputSignal = np.stack((outputSignal, outputChannel), axis=1)
            errorSignal = np.stack((errorSignal, errorChannel), axis=1)

    return outputSignal, errorSignal


def process_prerecorded(device, inputFile, targetFile, truncateSize, algorithm):
    inputSignal, inputFs = sf.read(inputFile, dtype='float32')
    targetSignal, targetFs = sf.read(targetFile, dtype='float32')

    # trucate the input signal for testing purposes as the file is big
    inputSignal = inputSignal[0:truncateSize]
    targetSignal = targetSignal[0:truncateSize]

    outputSignal, errorSignal = process_signal(
        inputSignal, targetSignal, algorithm)

    # player.play_signal(parser, outputSignal, inputFs, device)

    plot.plot_vertical(algorithm, 'prerecorded', inputSignal,
                       targetSignal, outputSignal, errorSignal)


# call back for the sounddevice Stream to perform live processing
def live_algorithm(algorithm, targetSignal, numChannels, indata, outdata, frames, time, status):
    global targetLocation
    global liveInputSignal
    global liveTargetSignal
    global liveOutputSignal
    global liveErrorSignal

    if status:
        print(status)

    # keep a running counter of where we are in the target signal
    # making a global variable for now
    inputSignal = np.array(indata)
    targetSignalMaxLength = len(targetSignal)
    truncateSize = len(inputSignal)
    targetEnd = (targetLocation + truncateSize)

    # start the target signal file over if we've reached the end
    if targetSignalMaxLength < targetEnd:
        targetLocation = 0

    # splice the target signal to line it up with the current input signal
    targetSignal = targetSignal[targetLocation:targetEnd]

    # process the signal and create pink noise
    if processing:
        outputSignal, errorSignal = process_signal(
        inputSignal, targetSignal, algorithm)
    else:
        outputSignal = np.add(inputSignal, targetSignal)
        errorSignal = np.zeros((len(targetSignal), 2))

    targetLocation += truncateSize
    outdata[:] = outputSignal

    #update global arrays for plotting
    if(liveInputSignal is None):
        liveInputSignal = inputSignal
        liveTargetSignal = targetSignal
        liveOutputSignal = outputSignal
        liveErrorSignal = errorSignal
    else:
        liveInputSignal = np.concatenate((liveInputSignal, inputSignal), axis=0)
        liveTargetSignal = np.concatenate((liveTargetSignal, targetSignal), axis=0)
        liveOutputSignal = np.concatenate((liveOutputSignal, outputSignal), axis=0)
        liveErrorSignal = np.concatenate((liveErrorSignal, errorSignal), axis=0)


def process_live(parser, device, targetFile, algorithm):
    global processing
    nextAction = ''

    try:
        numChannels = 2
        targetSignal, targetFs = sf.read(targetFile, dtype='float32')
        algo_partial = partial(
            live_algorithm, algorithm, targetSignal, numChannels)
        with sd.Stream(device=(device, device),
                    channels=numChannels, callback=algo_partial):
            while nextAction.upper() != 'EXIT':
                nextAction = input()
                if(nextAction.upper() == 'PAUSE' or nextAction.upper() == 'RESUME'):
                    processing = not processing
                
        
        # plot the results on exit
        plot.plot_vertical(algorithm, 'live', liveInputSignal,
                       liveTargetSignal, liveOutputSignal, liveErrorSignal)

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))


def process_anc(parser, device, targetFile, algorithm, btmode):
    try:
        if(btmode == 'server'):
            anc_server(device, targetFile, algorithm)
        elif(btmode == 'client'):
            anc_client(device)

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))


def anc_error_microphone_listener(indata, frames, time, status):
    global errorBuffer
    errorBuffer = np.concatenate((errorBuffer, indata), axis=0)
    print('errorBuffer', errorBuffer)


def setup_error_microphone_buffer(device):
    with sd.InputStream(device=(device, device), 
                         blocksize=128, #make an env var
                         channels=2,
                         callback=anc_error_microphone_listener):
        input()

def anc_output_listener(outdata, frames, time, status):
    global outputBuffer
    outputChunk = outputBuffer[slice(128), :] #make env var
    print('output chunk', outputChunk)
    if(np.shape(outputChunk)[0] == 128):
        outdata[:] = outputChunk
        outputBuffer = np.delete(outputBuffer,slice(128), 0)
    

def setup_output_stream(device):
    with sd.OutputStream(device=(device, device), 
                         blocksize=128, #make an env var
                         channels=2,
                         callback=anc_output_listener):
        input()


def setup_reference_microphone_buffer(device):
    #global referenceBuffer
    #server_socket = btserver.configure_server()
    #client_socket = btserver.wait_on_client_connection(server_socket)

    # start listening to error microphone now that connection is made
    thread.start_new_thread( setup_error_microphone_buffer, (device,) )
    thread.start_new_thread( setup_output_stream, (device,) )

    #while True:
    #    packet = client_socket.recv(1024) #make an env var
    #    if not packet: break
    #    referenceBuffer.append(packet)

    #btserver.close_connection(client_socket, server_socket)


def process_server_buffers():
    global errorBuffer
    global referenceBuffer
    global outputBuffer
    
    # output the error buffer for testing
    if(np.shape(errorBuffer)[0] >= 128): #make env var
        errorChunk = errorBuffer[slice(128), :] #make env var
        outputBuffer = np.concatenate((outputBuffer, errorChunk), axis=0)
        errorBuffer = np.delete(errorBuffer,slice(128), 0)
        # play the chunk for testing output in this mode


def anc_server(device, targetFile, algorithm):
    # setup thread for the reference microphone
    thread.start_new_thread( setup_reference_microphone_buffer, (device, ) )

    # setup an infinite loop to process the buffers simultaneously
    process_server_buffers()


def anc_client_listener(client_socket, indata, frames, time, status):
    print('shape: ', indata.shape)
    reference_data = pickle.dumps(indata)
    print('size of ref_data:', sys.getsizeof(reference_data))
    btclient.send_data(client_socket, reference_data)
    print('ACK')


def anc_client(device):
    global processing
    nextAction = ''
    client_socket = btclient.configure_client()

    algo_partial = partial(anc_client_listener, client_socket)
    with sd.InputStream(device=(device, device),
                        blocksize=128,
                        channels=2,
                        callback=algo_partial):
        while nextAction.upper() != 'EXIT':
            nextAction = input()
            if(nextAction.upper() == 'PAUSE' or nextAction.upper() == 'RESUME'):
                processing = not processing

    btclient.close_connection(client_socket)
    

import numpy as np

from functools import partial
from profilehooks import profile

import sys

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

def anc_server(device, targetFile, algorithm):
    server_socket = btserver.configure_server()
    client_socket = btserver.wait_on_client_connection(server_socket)
    client_data = ''

    while(client_data is not None):
        client_data = btserver.receive_frame(client_socket)
        print(client_data)
    
    btserver.close_connection(client_socket, server_socket)

def anc_client(device):
    i = 0
    client_socket = btclient.configure_client()

    while(i < 5):
        result = btclient.send_data(client_socket, i)
        print(result)
        i += 1
    
    btclient.close_connection(client_socket)
    
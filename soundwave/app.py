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

mu = 0.00001
targetLocation = 0
liveInputSignal = None
liveTargetSignal = None
liveOutputSignal = None
liveErrorSignal = None

def lms(inputSignal, targetSignal, numChannels):
    return lmsalgos.lms(inputSignal, targetSignal, mu, numChannels)

def clms(inputSignal, targetSignal, numChannels):
    return lmsalgos.clms(inputSignal, targetSignal, mu, numChannels)

def nlms(inputSignal, targetSignal, numChannels):
    return lmsalgos.nlms(inputSignal, targetSignal, mu, numChannels)


def nsslms(inputSignal, targetSignal, numChannels):
    return lmsalgos.nsslms(inputSignal, targetSignal, mu, numChannels)

def rls(inputSignal, targetSignal, numChannels):
    return lmsalgos.rls(inputSignal, targetSignal, mu, numChannels)

def crls(inputSignal, targetSignal, numChannels):
    return lmsalgos.crls(inputSignal, targetSignal, mu, numChannels)

def run_algorithm(algorithm, inputSignal, targetSignal, numChannels):
    switcher = {
        'lms': partial(lms, inputSignal, targetSignal, numChannels),
        'nlms': partial(nlms, inputSignal, targetSignal, numChannels),
        'nsslms': partial(nsslms, inputSignal, targetSignal, numChannels),
        'rls': partial(rls, inputSignal, targetSignal, numChannels),
        'clms': partial(clms, inputSignal, targetSignal, numChannels),
        'crls': partial(crls, inputSignal, targetSignal, numChannels)
    }

    # Get the function from switcher dictionary
    func = switcher.get(algorithm)
    # Execute the function
    return func()

#@profile(immediate=True)
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


# we need to do the actual processing here for the algorithm.
# can we use a partial function to inject the information
# about the algorithm chosen and the targetFile


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
    outputSignal, errorSignal = process_signal(
        inputSignal, targetSignal, algorithm)

    targetLocation += truncateSize
    outdata[:] = indata

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
    #raise ValueError('A very specific bad thing happened.')


def process_live(parser, device, targetFile, algorithm):
    try:
        numChannels = 2
        targetSignal, targetFs = sf.read(targetFile, dtype='float32')
        algo_partial = partial(
            live_algorithm, algorithm, targetSignal, numChannels)
        with sd.Stream(device=(device, device),
                    channels=numChannels, callback=algo_partial):
            input()
    except KeyboardInterrupt:
        #now that we have interrupted the recording, plot the results
        plot.plot_vertical(algorithm, 'live', liveInputSignal,
                       liveTargetSignal, liveOutputSignal, liveErrorSignal)
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))

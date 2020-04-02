import numpy as np

from functools import partial

import sys

import sounddevice as sd
import soundfile as sf

import soundwave.algorithms.least_mean_squares as lmsalgos
import soundwave.playback.playback as player
import soundwave.microphone.microphone as mic
import soundwave.plotting.plot as plot

mu = 0.00001


def lms(inputSignal, targetSignal, numChannels):
    return lmsalgos.lms(inputSignal, targetSignal, mu, numChannels)


def nlms(inputSignal, targetSignal, numChannels):
    return lmsalgos.nlms(inputSignal, targetSignal, mu, numChannels)


def nsslms(inputSignal, targetSignal, numChannels):
    return lmsalgos.nsslms(inputSignal, targetSignal, mu, numChannels)


def run_algorithm(algorithm, inputSignal, targetSignal, numChannels):
    switcher = {
        'lms': partial(lms, inputSignal, targetSignal, numChannels),
        'nlms': partial(nlms, inputSignal, targetSignal, numChannels),
        'nsslms': partial(nsslms, inputSignal, targetSignal, numChannels),
    }

    # Get the function from switcher dictionary
    func = switcher.get(algorithm)
    # Execute the function
    return func()


def process_prerecorded(parser, device, inputFile, targetFile, truncateSize, algorithm):
    try:
        inputSignal, inputFs = sf.read(inputFile, dtype='float32')
        targetSignal, targetFs = sf.read(targetFile, dtype='float32')

        # trucate the input signal for testing purposes as the file is big
        inputSignal = inputSignal[0:truncateSize]
        targetSignal = targetSignal[0:truncateSize]

        # loop over each channel and perform the algorithm
        numChannels = len(inputSignal[0])
        outputSignal = None
        errorSignal = None
        for channel in range(numChannels):
            # convert the signals to matrix structure so that
            # we can have a column based approach
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

        # player.play_signal(parser, outputSignal, inputFs, device)

        plot.plot_vertical(algorithm, inputSignal,
                           targetSignal, outputSignal, errorSignal)

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))


# we need to do the actual processing here for the algorithm.
# can we use a partial function to inject the information
# about the algorithm chosen and the targetFile
def live_algorithm(algorithm, targetSignal, numChannels, indata, outdata, frames, time, status):
    if status:
        print(status)

    outputSignal = None
    errorSignal = None
    for channel in range(numChannels):
        inputChannel = np.asmatrix(indata[:, channel])
        inputChannel = inputChannel.T

        targetChannel = np.asmatrix(targetSignal[:, channel])
        targetChannel = targetChannel.T

        inputChannel = np.hstack((inputChannel, targetChannel))
        inputChannel = np.asarray(inputChannel)

        # perform algorithm on left channel, then right right
        outputChannel, errorChannel = run_algorithm(
            algorithm, inputChannel, targetChannel, 0, numChannels)

        if outputSignal is None:
            outputSignal = outputChannel
            errorSignal = errorChannel
        else:
            outputSignal = np.stack((outputSignal, outputChannel), axis=1)
            errorSignal = np.stack((errorSignal, errorChannel), axis=1)

    outdata[:] = outputSignal


def process_live(parser, device, targetFile, algorithm):
    try:
        numChannels = 2
        targetSignal, targetFs = sf.read(targetFile, dtype='float32')
        algo_partial = partial(
            live_algorithm, algorithm, targetSignal, numChannels)
        with sd.Stream(device=(device, device),
                       samplerate=targetFs,
                       channels=numChannels, callback=algo_partial):
            print('#' * 80)
            print('press Return to quit')
            print('#' * 80)
            input()

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))

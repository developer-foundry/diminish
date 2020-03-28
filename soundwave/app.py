import numpy as np

from functools import partial

import sys
import queue

import sounddevice as sd
import soundfile as sf

import soundwave.algorithms.least_mean_squares as lmsalgos
import soundwave.playback.playback as player
import soundwave.microphone.microphone as mic
import soundwave.plotting.plot as plot

mu = 0.00001
q = queue.Queue()


def lms(inputSignal, targetSignal, channel, numChannels):
    return lmsalgos.lms(inputSignal, targetSignal, mu, numChannels)


def nlms(inputSignal, targetSignal, channel, numChannels):
    return lmsalgos.nlms(inputSignal, targetSignal[:, channel], mu, numChannels)


def nsslms(inputSignal, targetSignal, channel, numChannels):
    return lmsalgos.nsslms(inputSignal, targetSignal[:, channel], mu, numChannels)


def run_algorithm(algorithm, inputSignal, targetSignal, channel, numChannels):
    switcher = {
        'lms': partial(lms, inputSignal, targetSignal, channel, numChannels),
        'nlms': partial(nlms, inputSignal, targetSignal, channel, numChannels),
        'nsslms': partial(nsslms, inputSignal, targetSignal, channel, numChannels),
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
            inputChannel = np.asmatrix(inputSignal[:, channel])
            inputChannel = inputChannel.T

            targetChannel = np.asmatrix(targetSignal[:, channel])
            targetChannel = targetChannel.T

            inputChannel = np.hstack((inputChannel, targetChannel))
            inputChannel = np.asarray(inputChannel)

            # perform algorithm on left channel, then right right
            outputChannel, errorChannel = run_algorithm(
                algorithm, inputChannel, targetChannel, 0, 2)

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


def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata)


def process_live(parser, device, targetFile, algorithm):
    try:
        targetSignal, targetFs = sf.read(targetFile, dtype='float32')

        # begin receive the input signal from the microphone
        inputStream = mic.record_to_stream(
            parser, device, 2, 44100, audio_callback)

        with inputStream:
            print('#' * 80)
            print('press Return to quit')
            print('#' * 80)
            input()

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))

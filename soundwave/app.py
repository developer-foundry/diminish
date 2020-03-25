import numpy as np

from functools import partial

import sounddevice as sd
import soundfile as sf

import soundwave.algorithms.least_mean_squares as lmsalgos
import soundwave.playback.playback as player
import soundwave.plotting.plot as plot

mu = 0.00001


def lms(inputSignal, targetSignal, channel, numChannels):
    #return lmsalgos.lms(inputSignal, targetSignal[:, channel], mu, numChannels)
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


def process(parser, device, inputFile, targetFile, truncateSize, algorithm):
    try:
        inputSignal, inputFs = sf.read(inputFile, dtype='float32')
        targetSignal, targetFs = sf.read(targetFile, dtype='float32')

        # trucate the input signal for testing purposes as the file is big
        inputSignal = inputSignal[0:truncateSize]
        inputSignal = np.asmatrix(inputSignal)
        inputSignal = inputSignal.T

        # first ensure that the targetData is the same size as the input data.
        #targetSignal = targetSignal[0:inputSignal.shape[0], :]
        targetSignal = targetSignal[0:truncateSize]
        targetSignalX = np.asmatrix(targetSignal)
        targetSignalX = targetSignalX.T

        inputSignal = np.hstack((inputSignal, targetSignalX))

        # perform algorithm on left channel, then right right
        outputLeftSignal, errorLeftSignal = run_algorithm(
            algorithm, inputSignal, targetSignal, 0, 2)

        #outputRightSignal, errorRightSignal = run_algorithm(
        #    algorithm, inputSignal, targetSignal, 1, 2)

        # combine left and right channels
        #outputSignal = np.column_stack((outputLeftSignal, outputRightSignal))
        #errorSignal = np.column_stack((errorLeftSignal, errorRightSignal))

        #player.play_signal(parser, outputLeftSignal, inputFs, device)

        plot.plot_vertical(algorithm, inputSignal,
                           targetSignal, outputLeftSignal, errorLeftSignal)

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))

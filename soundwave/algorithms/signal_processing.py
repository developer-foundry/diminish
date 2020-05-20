import logging
from functools import partial
import numpy as np
from soundwave.algorithms.crls import crls
from common.common import mu
import os


def run_algorithm(algorithm, inputSignal, targetSignal, numChannels):
    switcher = {
        'crls': partial(crls, inputSignal, targetSignal, mu, numChannels)
    }

    func = switcher.get(algorithm)
    return func()


def process_signal(inputSignal, targetSignal, algorithm):
    numChannels = 2
    outputSignal = None
    errorSignal = None

    # loop over each channel and perform the algorithm
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

import logging
from functools import partial
import numpy as np
import soundwave.algorithms.least_mean_squares as lmsalgos
from soundwave.common.common import mu

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
    numChannels = len(inputSignal[0]) // 2 # assumes that error and a single reference microphone are combined
    outputSignal = None
    errorSignal = None
    logging.info(f'targetSignal size: {targetSignal.shape}')
    for channel in range(numChannels):
        logging.info(f'channel: {channel}')
        targetChannel = targetSignal[:, channel]
        inputChannel = np.stack((inputSignal[:, channel],
                                 inputSignal[:, (channel + 2)]), axis=1)
        logging.info(f'input size: {inputChannel.shape}')
        inputChannel = np.column_stack([inputChannel, targetChannel])
        logging.info(f'inputChannel size: {inputChannel.shape}')
        logging.info(f'targetChannel size: {targetChannel.shape}')

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
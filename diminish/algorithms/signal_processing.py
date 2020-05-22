import logging
from functools import partial
import numpy as np
from diminish.algorithms.crls import crls
from common.common import mu
import os


def run_algorithm(algorithm, inputSignal, targetSignal, numChannels):
    """Selects a specific algorithm to use to process signa. Currently, there is only one algorithm implemented,
    additional algorithms can be added here.

    Parameters
    ----------
    algorithm : str
        The name of the algorithm used to perform ANC. Currently, only 'crls' is available.
    inputSignal : np.array
        Input matrix (2-dimensional array). Rows are samples. Columns are input arrays.
    targetSignal : np.array
        Target matrix (2-dimensional array). Rows are samples. Columns are input arrays.
    numChannels : int
        The number of channels in the input signal. Likely to always be 2.

    Returns
    -------
    y : np.array
        An array of data representing the output signal
    e : np.array
        Ar array of data representing the error singal

    Raises
    ------
    None
    """
    switcher = {
        'crls': partial(crls, inputSignal, targetSignal, mu, numChannels)
    }

    func = switcher.get(algorithm)
    return func()


def process_signal(inputSignal, targetSignal, algorithm):
    """Processes input signal to try and achieve an output that is closest to target signal by running an ANC algorithm

    Parameters
    ----------
    algorithm : str
        The name of the algorithm used to perform ANC. Currently, only 'crls' is available.
    inputSignal : np.array
        Input matrix (2-dimensional array). Rows are samples. Columns are input arrays.
    targetSignal : np.array
        Target matrix (2-dimensional array). Rows are samples. Columns are input arrays.

    Returns
    -------
    outputSignal : np.array
        An array of data representing the output signal
    errorSignal : np.array
        Ar array of data representing the error singal

    Raises
    ------
    None
    """
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

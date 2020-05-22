"""
This script shares common functions and variables needed to plot signal data
"""

import matplotlib  # nopep8
matplotlib.use('Agg')  # nopep8
import os
import matplotlib.pyplot as plt
import logging
import time

def get_dir(algorithm, mode):
    """
    Used to determine the plotting folder 

    Parameters
    ----------
    algorithm: String
        The name of the current ANC algorithm running
    mode: String
        The MODE (precorded or anc) the server is currently running

    Returns
    -------
    path : Path
        The path of the plots directory of diminish

    Raises
    ------
    None
    """
    base_dir = os.getcwd()
    results_dir = os.path.join(base_dir, f'plots/{algorithm}/{mode}/')
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    return results_dir

def plot_vertical(algorithm, mode, inputSignal, targetSignal, outputSignal, errorSignal):
    """
    Plots the necessary signals for prerecorded mode

    Parameters
    ----------
    algorithm: String
        The name of the current ANC algorithm running
    mode: String
        The MODE (precorded or anc) the server is currently running
    inputSignal: np.array
        The reference microphone signal
    targetSignal: np.array
        The desired target signal the user should hear
    outputSignal: np.array
        The actual speaker output the user hears
    errorSignal: np.array
        The difference between the output signal and the target signal

    Returns
    -------
    None

    Raises
    ------
    None
    """
    algDirectory = get_dir(algorithm, mode)

    fig, axs = plt.subplots(4)
    fig.set_size_inches(18.5, 10.5)
    fig.tight_layout(pad=3.0)
    axs[0].plot(inputSignal, '-b')
    axs[0].title.set_text(f'{algorithm} Input Signal')
    axs[0].set_ylim((-0.4, 0.4))
    axs[1].plot(targetSignal, '-g')
    axs[1].title.set_text(f'{algorithm} Target Signal')
    axs[1].set_ylim((-0.4, 0.4))
    axs[2].plot(outputSignal, '-k')
    axs[2].title.set_text(f'{algorithm} Output Signal')
    axs[2].set_ylim((-0.4, 0.4))
    axs[3].plot(errorSignal, '-r')
    axs[3].title.set_text(f'{algorithm} Error Signal')
    axs[3].set_ylim((-0.4, 0.4))
    plt.savefig(algDirectory + f'{algorithm}- allsignals.png')

def plot_vertical_buffers(algorithm, mode, buffers):
    """
    Plots the error, reference, output, target, and output error
    signals for ANC mode

    Parameters
    ----------
    algorithm: String
        The name of the current ANC algorithm running
    mode: String
        The MODE (precorded or anc) the server is currently running
    buffers: list
        The list of buffers to plot

    Returns
    -------
    None

    Raises
    ------
    None
    """
    logging.debug(f'Plotting colors')

    colors = ['-b', '-m', '-g', '-k', '-r']
    algDirectory = get_dir(algorithm, mode)

    fig, axs = plt.subplots(len(buffers))
    fig.set_size_inches(18.5, 10.5)
    fig.tight_layout(pad=3.0)

    max = 0
    for index, bufferName in enumerate(buffers):
        if len(buffers[bufferName]) > max:
            max = len(buffers[bufferName])

    for index, bufferName in enumerate(buffers):
        axs[index].plot(buffers[bufferName], colors[index])
        axs[index].title.set_text(f'{algorithm} {bufferName} Signal')
        axs[index].set_ylim((-0.4, 0.4))
        axs[index].set_xlim((0, max))

    timestr = time.strftime("%Y%m%d-%H%M%S")
    plt.savefig(algDirectory + f'{algorithm}- allsignals - {timestr}.png')

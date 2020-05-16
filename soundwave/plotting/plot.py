import matplotlib  # nopep8
matplotlib.use('Agg')  # nopep8
import os
import matplotlib.pyplot as plt
import logging

def get_dir(algorithm, mode):
    base_dir = os.getcwd()
    results_dir = os.path.join(base_dir, f'plots/{algorithm}/{mode}/')
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    return results_dir


def plot_simultaneous(algorithm, mode, inputSignal, targetSignal, outputSignal):
    algDirectory = get_dir(algorithm, mode)

    plt.plot(inputSignal, '-b')
    plt.savefig(algDirectory + f'{algorithm}_input.png')

    plt.plot(targetSignal, '-g')
    plt.savefig(algDirectory + f'{algorithm}_target.png')

    plt.plot(outputSignal, '-r')
    plt.savefig(algDirectory + f'{algorithm}_output.png')


def plot_vertical(algorithm, mode, inputSignal, targetSignal, outputSignal, errorSignal):
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
    colors = ['-b', '-m', '-g', '-k', '-r']
    algDirectory = get_dir(algorithm, mode)

    fig, axs = plt.subplots(len(buffers))
    fig.set_size_inches(18.5, 10.5)
    fig.tight_layout(pad=3.0)

    for index, bufferName in enumerate(buffers):
        axs[index].plot(buffers[bufferName], colors[index])
        axs[index].title.set_text(f'{algorithm} {bufferName} Signal')
        #axs[index].set_ylim((-0.4, 0.4))

    plt.savefig(algDirectory + f'{algorithm}- allsignals.png')

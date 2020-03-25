import matplotlib  # nopep8
matplotlib.use('Agg')  # nopep8
import os
import matplotlib.pyplot as plt


def get_dir(algorithm):
    base_dir = os.getcwd()
    results_dir = os.path.join(base_dir, 'plots/% s/' % (algorithm))
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    return results_dir


def plot_simultaneous(algorithm, inputSignal, targetSignal, outputSignal):
    algDirectory = get_dir(algorithm)

    plt.plot(inputSignal, '-b')
    plt.savefig(algDirectory + 'input.png')

    plt.plot(targetSignal, '-g')
    plt.savefig(algDirectory + 'target.png')

    plt.plot(outputSignal, '-r')
    plt.savefig(algDirectory + 'output.png')


def plot_vertical(algorithm, inputSignal, targetSignal, outputSignal):
    algDirectory = get_dir(algorithm)

    fig, axs = plt.subplots(3)
    fig.suptitle('Signals Stacked')
    axs[0].plot(inputSignal, '-b')
    axs[1].plot(targetSignal, '-g')
    axs[2].plot(outputSignal, '-r')
    plt.savefig(algDirectory + 'allsignals.png')

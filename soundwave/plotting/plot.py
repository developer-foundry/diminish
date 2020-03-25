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


def plot_vertical(algorithm, inputSignal, targetSignal, outputSignal, errorSignal):
    algDirectory = get_dir(algorithm)

    fig, axs = plt.subplots(4)
    fig.set_size_inches(18.5, 10.5)
    fig.tight_layout(pad=3.0)
    axs[0].plot(inputSignal, '-b')
    axs[0].title.set_text('% s Input Signal' % algorithm)
    axs[1].plot(targetSignal, '-g')
    axs[1].title.set_text('% s Target Signal' % algorithm)
    axs[2].plot(outputSignal, '-y')
    axs[2].title.set_text('% s Output Signal' % algorithm)
    axs[3].plot(errorSignal, '-r')
    axs[3].title.set_text('% s Error Signal' % algorithm)
    plt.savefig(algDirectory + 'allsignals.png')

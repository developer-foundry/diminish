import matplotlib  # nopep8
matplotlib.use('Agg')  # nopep8
import os
import matplotlib.pyplot as plt


def plot_simultaneous(algorithm, inputSignal, targetSignal, outputSignal):
    base_dir = os.getcwd()
    results_dir = os.path.join(base_dir, 'plots/% s/' % (algorithm))
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    plt.plot(inputSignal, '-b')
    plt.savefig(results_dir + 'input.png')

    plt.plot(targetSignal, '-g')
    plt.savefig(results_dir + 'target.png')

    plt.plot(outputSignal, '-r')
    plt.savefig(results_dir + 'output.png')

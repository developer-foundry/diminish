import matplotlib  # nopep8
matplotlib.use('Agg')  # nopep8

import matplotlib.pyplot as plt


def plot_simultaneous(inputSignal, targetSignal, outputSignal):
    plt.plot(inputSignal, '-b')
    plt.savefig('plots/input.png')

    plt.plot(targetSignal, '-g')
    plt.savefig('plots/target.png')

    plt.plot(outputSignal, '-r')
    plt.savefig('plots/output.png')

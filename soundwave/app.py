from __future__ import print_function  # nopep8
import numpy as np  # nopep8
import matplotlib  # nopep8
matplotlib.use('Agg')  # nopep8

import matplotlib.pyplot as plt
import sys
import time

import alsaaudio
import sounddevice as sd
import soundfile as sf

import soundwave.algorithms.least_mean_squares as lms


def acn_file(parser, device, inputSignal, targetSignal):
    try:
        inputData, inputFs = sf.read(inputSignal, dtype='float32')
        targetData, targetFs = sf.read(targetSignal, dtype='float32')

        # trucate the input signal for testing purposes as the file is big
        inputData = inputData[0:300000]

        # first ensure that the targetData is the same size as the input data.
        targetData = targetData[0:inputData.shape[0], :]

        # perform lms on left channel, then right right
        outputLeftSignal, errorLeftSignal = lms.least_mean_squares(
            inputData, targetData[:, 0], 0.1, 2)

        outputRightSignal, errorRightSignal = lms.least_mean_squares(
            inputData, targetData[:, 1], 0.1, 2)

        # combine left and right channels
        outputSignal = np.column_stack((outputLeftSignal, outputRightSignal))

        sd.play(outputSignal, inputFs, device=device)
        status = sd.wait()
        if status:
            parser.exit('Error during playback: ' + str(status))

        plt.plot(inputData, '-b')
        plt.savefig('plots/input.png')

        plt.plot(targetData, '-g')
        plt.savefig('plots/target.png')

        plt.plot(outputSignal, '-r')
        plt.savefig('plots/output.png')
    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))


def play(parser, device, f):

    try:
        data, fs = sf.read(f, dtype='float32')
        sd.play(data, fs, device=device)
        status = sd.wait()
        if status:
            parser.exit('Error during playback: ' + str(status))

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))


def record(parser, device, f):
    duration = 5  # seconds
    frequency = 44100
    myrecording = sd.rec(int(duration * frequency),
                         samplerate=frequency, channels=2)
    sd.wait()
    sf.write(f, myrecording, frequency)

from __future__ import print_function
import numpy as np
import matplotlib # Do not move this
matplotlib.use('Agg') # Do not move this

import matplotlib.pyplot as plt
import sys
import time

import alsaaudio
import sounddevice as sd
import soundfile as sf


def acn_file(parser, device, f):
    try:
        data, fs = sf.read(f, dtype='float32')
        sd.play(data, fs, device=device)
        status = sd.wait()
        if status:
            parser.exit('Error during playback: ' + str(status))

        plt.plot(data, '-b')
        plt.savefig('plots/test.png')
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

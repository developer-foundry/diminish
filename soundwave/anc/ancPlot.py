import sys
import threading
import logging

import numpy as np

import sounddevice as sd
from common.continuousBuffer import ContinuousBuffer
import soundwave.plotting.plot as plot

class AncPlot():
    def __init__(self, buffers):
        self.buffers = {} #dictionary to hold the data that is popped off buffers for ploting

        for buffer in buffers:
            self.buffers[buffer.name] = np.empty((0,2))
            buffer.subscribe(self.observe)

    def observe(self, bufferName, data):
        self.buffers[bufferName] = np.concatenate((self.buffers[bufferName], data), axis=0)

    def plot_buffers(self, algorithm):
        plot.plot_vertical_buffers(algorithm, 'anc', self.buffers)

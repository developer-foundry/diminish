import sys
import threading
import logging

import numpy as np

import sounddevice as sd
from common.continuousBuffer import ContinuousBuffer
import soundwave.plotting.plot as plot
import threading
from multiprocessing.connection import Listener

class AncPlot():
    def __init__(self, buffers):
        self.buffers = {} #dictionary to hold the data that is popped off buffers for ploting
        self.dataClient = None #used by the TUI application to pass data
        for buffer in buffers:
            self.buffers[buffer.name] = np.empty((0,2))
            buffer.subscribe(self.observe)

    def observe(self, bufferName, data):
        self.buffers[bufferName] = np.concatenate((self.buffers[bufferName], data), axis=0)

    def plot_buffers(self, algorithm):
        plot.plot_vertical_buffers(algorithm, 'anc', self.buffers)

    def sendData(self):
        if(len(self.buffers['error']) > 0):
            self.dataClient.send(self.buffers['error'][-1])

        threading.Timer(1.0, self.sendData).start()
        
    def create_connection(self):
        self.listener = Listener(('localhost', 5000), authkey=b'secret password')
        logging.debug('Connecting Server...')
        self.dataClient = self.listener.accept()
        logging.debug('Connected Server...')
        self.sendData()

    def close_connection(self):
        if(self.dataClient is not None):
            self.dataClient.close()
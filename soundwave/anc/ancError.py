import sys
import threading
import logging

import numpy as np
from blinker import signal

import sounddevice as sd

class AncError(threading.Thread):
    def __init__(self, device, threadName):
        threading.Thread.__init__(self, name=threadName)
        self.onError = signal('anc_error_errors')
        self.device = device
        self.errorBuffer = np.arange(2).reshape(1,2)

    def listener(self, indata, frames, time, status):
        logging.debug('The error microphone is processing data in the shape: %d %d' % (indata.shape[0], indata.shape[1]))
        self.errorBuffer = np.concatenate((self.errorBuffer, indata), axis=0) #concatenate seems to be slow at a certain size

    def run(self):
        try:
            with sd.InputStream(device=(self.device, self.device),
                        blocksize=128,
                        channels=2,
                        callback=self.listener):
                input()
        except Exception as e:
            self.onError.send(e)
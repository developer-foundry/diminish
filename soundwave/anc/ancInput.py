import sys
import threading
import logging

import numpy as np
from blinker import signal

import sounddevice as sd
from soundwave.common.continuousBuffer import ContinuousBuffer

class AncInput(threading.Thread):
    def __init__(self, device, buffer, threadName):
        logging.debug('Initialize Input Microphone thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.buffer = buffer
        self.device = device

    def listener(self, indata, frames, time, status):
        self.buffer.push(indata)

    def run(self):
        try:
            logging.debug('Running Input Microphone thread')
            with sd.InputStream(device=self.device,
                                channels=2,
                                callback=self.listener):
                input()

        except Exception as e:
            logging.error(f'Exception thrown: {e}')

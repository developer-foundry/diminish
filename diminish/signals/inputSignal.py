import sys
import threading
import logging
import time
import numpy as np

import sounddevice as sd
from common.continuousBuffer import ContinuousBuffer


class InputSignal(threading.Thread):
    def __init__(self, device, buffer, stepSize, threadName):
        logging.debug('Initialize Input Microphone thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.buffer = buffer
        self.device = device
        self.stepSize = stepSize
        self.stopped = False

    def listener(self, indata, frames, time, status):
        self.buffer.push(indata)

    def stop(self):
        self.stopped = True

    def run(self):
        try:
            logging.debug('Running Input Microphone thread')

            with sd.InputStream(device=self.device,
                                channels=2,
                                blocksize=self.stepSize,
                                callback=self.listener):
                while not self.stopped:
                    time.sleep(1)  # time takes up less cpu cycles than 'pass'

        except Exception as e:
            logging.exception(f'Exception thrown: {e}')

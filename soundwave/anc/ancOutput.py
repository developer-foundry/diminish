import sys
import threading
import logging

import numpy as np
from blinker import signal
import sounddevice as sd


class AncOutput(threading.Thread):
    def __init__(self, device, buffer, waitCondition, threadName):
        logging.debug('Initializing Output Speaker thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.device = device
        self.buffer = buffer
        self.waitCondition = waitCondition

    def listener(self, outdata, frames, time, status):
        data = self.buffer.pop()
        size = data.shape[0]
        outdata[:size] = data

    def run(self):
        try:
            logging.debug('Running Output Speaker thread')
            with self.waitCondition:
                self.waitCondition.wait()

                with sd.OutputStream(device=self.device,
                                channels=2,
                                callback=self.listener):
                    input()

        except Exception as e:
            logging.error(f'Exception thrown: {e}')

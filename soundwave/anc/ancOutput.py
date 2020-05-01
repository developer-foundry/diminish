import sys
import threading
import logging

import numpy as np
from blinker import signal
import sounddevice as sd


class AncOutput(threading.Thread):
    def __init__(self, device, buffer, threadName):
        logging.debug('Initializing Output Speaker thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.device = device
        self.buffer = buffer

    def listener(self, outdata, frames, time, status):
        if(self.buffer.is_ready()):
            outdata[:self.buffer.stepSize] = self.buffer.pop()

    def run(self):
        try:
            logging.debug('Running Output Speaker thread')
            with sd.OutputStream(device=self.device,
                            channels=2,
                            callback=self.listener):
                input()

        except Exception as e:
            logging.error(f'Exception thrown: {e}')

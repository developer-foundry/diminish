import sys
import threading
import logging

import numpy as np
from blinker import signal

import sounddevice as sd


class AncInput(threading.Thread):
    def __init__(self, device, threadName):
        threading.Thread.__init__(self, name=threadName, daemon=True)
        logging.debug('Initialize Input Microphone thread')
        self.onError = signal('anc_input_errors')
        self.onData = signal('anc_input_data')
        self.device = device
        self._stop = threading.Event()

    def stop(self):
        logging.debug('Stopping Input Microphone thread')
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def cleanup(self):
        logging.debug('Cleaning up Input Microphone thread')

    def listener(self, indata, frames, time, status):
        self.onData.send(indata)

    def run(self):
        try:
            logging.debug('Running Input Microphone thread')
            with sd.InputStream(device=self.device,
                                channels=2,
                                callback=self.listener):
                input()

            self.cleanup()
        except Exception as e:
            self.onError.send(e)

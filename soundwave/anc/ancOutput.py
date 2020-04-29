import sys
import threading
import logging

import numpy as np
from blinker import signal
import sounddevice as sd


class AncOutput(threading.Thread):
    def __init__(self, device, threadName):
        threading.Thread.__init__(self, name=threadName, daemon=True)
        logging.debug('Initializing Output Speaker thread')

        # Signals
        self.onError = signal('anc_output_errors')
        self.onData = signal('anc_output_data')
        self.onReady = signal('anc_ready')

        # Devices
        self.device = device

        # Buffers
        self.outputBuffer = np.zeros((0, 2))

        self._stop = threading.Event()

    def stop(self):
        logging.debug('Stopping Output Speaker thread')
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def cleanup(self):
        logging.debug('Cleaning up Output Speaker thread')

    def listener(self, outdata, frames, time, status):
        if(np.shape(self.outputBuffer)[0] > 0):
            outdata[:len(self.outputBuffer)] = self.outputBuffer
            self.outputBuffer = np.zeros(0,2)

    def receiveOutput(self, data):
        logging.debug(f'Receiving data for Output Speaker thread:')
        logging.debug(data)
        self.outputBuffer = np.append(self.outputBuffer, data)

    def initializeOutputStream(self, is_ready):
        if is_ready:
            logging.debug(f'Setting up the output stream for processing:')
            with sd.OutputStream(device=self.device,
                                channels=2,
                                callback=self.listener):
                input()

    def run(self):
        try:
            logging.debug('Running Output Speaker thread')
            self.onData.connect(self.receiveOutput)
            self.onReady.connect(self.initializeOutputStream)

            while True:
                i = 0

        except Exception as e:
            self.onError.send(e)

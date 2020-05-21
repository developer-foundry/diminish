import sys
import threading
import logging
import time

import numpy as np
import sounddevice as sd


class OutputSignal(threading.Thread):
    def __init__(self, device, buffer, stepSize, waitCondition, threadName):
        logging.debug('Initializing Output Speaker thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.device = device
        self.buffer = buffer
        self.stepSize = stepSize
        self.waitCondition = waitCondition
        self.stopped = False

    def listener(self, outdata, frames, time, status):
        data = self.buffer.pop()
        size = data.shape[0]
        outdata[:size] = data

    def stop(self):
        self.stopped = True

    def run(self):
        try:
            logging.debug('Running Output Speaker thread')
            with self.waitCondition:
                self.waitCondition.wait()

                with sd.OutputStream(device=self.device,
                                     channels=2,
                                     blocksize=self.stepSize,
                                     callback=self.listener):
                    while not self.stopped:
                        # time takes up less cpu cycles than 'pass'
                        time.sleep(1)

        except Exception as e:
            logging.exception(f'Exception thrown: {e}')
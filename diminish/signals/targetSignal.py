import sys
import threading
import logging

import numpy as np

import soundfile as sf
from common.continuousBuffer import ContinuousBuffer


class TargetSignal(threading.Thread):
    def __init__(self, targetFile, buffer, stepSize, size, threadName):
        logging.debug('Initialize Target File thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.buffer = buffer
        self.stepSize = stepSize
        self.size = size
        self.targetFile = targetFile
        self.targetSignal = None
        self.stopped = False

    def stop(self):
        self.stopped = True

    def run(self):
        try:
            # this thread does not keep running. it will end as soon as the buffer is populated
            logging.debug('Running Target File thread')
            self.targetSignal, _ = sf.read(
                self.targetFile, dtype='float32')
            self.buffer.push(self.targetSignal[0:self.size])

        except Exception as e:
            logging.exception(f'Exception thrown: {e}')

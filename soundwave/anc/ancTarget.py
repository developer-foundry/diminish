import sys
import threading
import logging

import numpy as np

import soundfile as sf
from soundwave.common.continuousBuffer import ContinuousBuffer

class AncTarget(threading.Thread):
    def __init__(self, targetFile, buffer, stepSize, threadName):
        logging.debug('Initialize Target File thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.buffer = buffer
        self.stepSize = stepSize
        self.targetFile = targetFile
        self.targetSignal = None

    def run(self):
        try:
            #this thread does not keep running. it will end as soon as the buffer is populated
            logging.debug('Running Target File thread')
            self.targetSignal, targetFs = sf.read(self.targetFile, dtype='float32')
            self.buffer.push(self.targetSignal)

        except Exception as e:
            logging.error(f'Exception thrown: {e}')

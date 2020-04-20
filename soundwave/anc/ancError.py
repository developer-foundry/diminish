import sys
import threading
import logging

import numpy as np
from blinker import signal

import sounddevice as sd

class AncError(threading.Thread):
    def __init__(self, device, threadName):
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.onError = signal('anc_error_errors')
        self.device = device
        self.errorBuffer = np.arange(2).reshape(1,2)
        self._stop = threading.Event() 
  
    def stop(self): 
        logging.debug('Stopping Error thread')
        self._stop.set()
  
    def stopped(self): 
        return self._stop.isSet()
    
    def cleanup(self):
        logging.debug('Cleaning up Error thread')

    def listener(self, indata, frames, time, status):
        logging.debug(f'The error microphone is processing data in the shape: {indata.shape[0]} {indata.shape[1]}')
        self.errorBuffer = np.concatenate((self.errorBuffer, indata), axis=0) #concatenate seems to be slow at a certain size
        logging.debug(f'The error buffer is now in the shape: {self.errorBuffer.shape[0]} {self.errorBuffer.shape[1]}')

    def run(self):
        try:
            with sd.InputStream(device=(self.device, self.device),
                        blocksize=128,
                        channels=2,
                        callback=self.listener):
                input()
            
            self.cleanup()
        except Exception as e:
            self.onError.send(e)
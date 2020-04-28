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
        self.onData = signal('anc_error_data')
        self.device = device
        self._stop = threading.Event() 
  
    def stop(self): 
        logging.debug('Stopping Error thread')
        self._stop.set()
  
    def stopped(self): 
        return self._stop.isSet()
    
    def cleanup(self):
        logging.debug('Cleaning up Error thread')

    def listener(self, indata, frames, time, status):
        self.onData.send(indata)

    def run(self):
        try:
            with sd.InputStream(device=(self.device, self.device),
                        channels=2,
                        callback=self.listener):
                input()
            
            self.cleanup()
        except Exception as e:
            self.onError.send(e)
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
        self.onError = signal('anc_output_errors')
        self.device = device
        self.outputBuffer = np.arange(2).reshape(1,2)
        self.onData = signal('anc_output_data')
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
            self.outputBuffer = np.arange(2).reshape(1,2)

    def receiveOutput(self, data):
        logging.debug(f'Receiving data for Output Speaker thread:')
        logging.debug(data)

    def run(self):
        try:
            logging.debug('Running Output Speaker thread')
            self.onData.connect(self.receiveOutput)
            with sd.OutputStream(device=(self.device, self.device), 
                         channels=2,
                         callback=self.listener):
                input()
            
            self.cleanup()
        except Exception as e:
            self.onError.send(e)
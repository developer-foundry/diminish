import sys
import threading
import logging

import numpy as np
from blinker import signal
import sounddevice as sd

class AncOutput(threading.Thread):
    def __init__(self, device, threadName):
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.onError = signal('anc_output_errors')
        self.device = device
        self.outputBuffer = np.arange(2).reshape(1,2)
        self.onData = signal('anc_output_data')
        self._stop = threading.Event() 
  
    def stop(self): 
        logging.debug('Stopping Output thread')
        self._stop.set()
  
    def stopped(self): 
        return self._stop.isSet()
    
    def cleanup(self):
        logging.debug('Cleaning up Output thread')
    
    def listener(self, outdata, frames, time, status):
        if(np.shape(self.outputBuffer)[0] > 0):
            outdata[:len(self.outputBuffer)] = self.outputBuffer
            self.outputBuffer = np.arange(2).reshape(1,2)

    def addOutputSignal(self, data):
        self.outputBuffer = np.append(self.outputBuffer, data, axis = 0)

    def run(self):
        try:
            self.onData.connect(self.addOutputSignal)
            with sd.OutputStream(device=(self.device, self.device), 
                         channels=2,
                         callback=self.listener):
                input()
            
            self.cleanup()
        except Exception as e:
            self.onError.send(e)
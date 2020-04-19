import sys
import threading
import logging

import numpy as np
from blinker import signal
import sounddevice as sd

class AncOutput(threading.Thread):
    def __init__(self, device, threadName):
        threading.Thread.__init__(self, name=threadName)
        self.onError = signal('anc_output_errors')
        self.device = device
        self.outputBuffer = np.arange(2).reshape(1,2)
    
    def listener(self, outdata, frames, time, status):
        outputChunk = self.outputBuffer[slice(128), :] #make env var
        logging.debug(f'The output speaker is processing data in the shape: {outputChunk.shape[0]} {outputChunk.shape[1]}')

        if(np.shape(outputChunk)[0] == 128):
            outdata[:] = outputChunk
            outputBuffer = np.delete(outputBuffer,slice(128), 0)

    def run(self):
        try:
            with sd.OutputStream(device=(self.device, self.device), 
                         blocksize=128, #make an env var
                         channels=2,
                         callback=self.listener):
                input()
        except Exception as e:
            self.onError.send(e)
import sys
import os
import threading
import logging

import numpy as np
from blinker import signal

import soundwave.bluetoothnetwork.server as btserver
from soundwave.anc.ancError import AncError
from soundwave.anc.ancOutput import AncOutput

class AncOrchestrator(threading.Thread):
    def __init__(self, device, algorithm, targetFile, threadName):
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.onError = signal('anc_orchestrator_errors')
        self.device = device
        self.referenceBuffer = []
        self.server_socket = None
        self.client_socket = None
        self.ancError = AncError(device, 'anc-error-main')
        self.ancOutput = AncOutput(device, 'anc-output-main')
        self._stop = threading.Event()
        self.algorithm = algorithm
        self.targetFile = targetFile
  
    def stop(self): 
        logging.debug('Stopping orchestrator thread')
        self._stop.set()
        self.ancError.stop()
        self.ancOutput.stop()
  
    def stopped(self): 
        return self._stop.isSet()
    
    def cleanup(self):
        logging.debug('Cleaning up orchestrator thread')
        btserver.close_connection(self.client_socket, self.server_socket)

    def run(self):
        try:
            self.server_socket = btserver.configure_server()
            self.client_socket = btserver.wait_on_client_connection(self.server_socket)

            if(self.client_socket is not None):
                self.ancError.start()
                self.ancOutput.start()

            while True:
                #check and see if the thread has been killed
                if(self.stopped()):
                    self.cleanup()
                    self.ancError.cleanup()
                    self.ancOutput.cleanup()
                    return

                packet = self.client_socket.recv(1024) #make an env var
                if not packet: 
                    break
                
                self.referenceBuffer.append(packet)
                logging.debug(f'Receiving data from the anc client. Size is : {sys.getsizeof(packet)}')

                #refactor to integrate with the error and output thread via blinker signals
                if(np.shape(self.ancError.errorBuffer)[0] >= 128): #make env var
                    errorChunk = self.ancError.errorBuffer[slice(128), :] #make env var
                    self.ancOutput.outputBuffer = np.concatenate((self.ancOutput.outputBuffer, errorChunk), axis=0)
                    self.ancError.errorBuffer = np.delete(self.ancError.errorBuffer,slice(128), 0)

                self.ancError.join(0.0)
                if self.ancError.stopped():
                    break

                self.ancOutput.join(0.0)
                if self.ancOutput.stopped():
                    break
            
            self.cleanup()
        except Exception as e:
            self.onError.send(e)
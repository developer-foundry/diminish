import sys
import threading
import logging

import numpy as np
from blinker import signal

import soundwave.bluetoothnetwork.server as btserver
from soundwave.anc.ancError import AncError
from soundwave.anc.ancOutput import AncOutput

class AncOrchestrator(threading.Thread):
    def __init__(self, device, threadName):
        threading.Thread.__init__(self, name=threadName)
        self.onError = signal('anc_orchestrator_errors')
        self.device = device
        self.referenceBuffer = []
        self.server_socket = None
        self.client_socket = None
        self.ancError = AncError(device, 'anc-error-main')
        self.ancOutput = AncOutput(device, 'anc-output-main')

    def run(self):
        try:
            self.server_socket = btserver.configure_server()
            self.client_socket = btserver.wait_on_client_connection(self.server_socket)
            self.ancError.start()
            self.ancOutput.start()

            while True:
                packet = self.client_socket.recv(1024) #make an env var
                if not packet: 
                    break
                
                self.referenceBuffer.append(packet)
                logging.debug(f'Receiving data from the anc client. Size is : {sys.getsizeof(packet)}')

                # refactor?
                self.ancError.join(0.1)
                if self.ancError.isAlive():
                    continue
                else:
                    break

                self.ancOutput.join(0.1)
                if self.ancOutput.isAlive():
                    continue
                else:
                    break

                #refactor to integrate with the error and output thread via blinker signals
                """
                if(np.shape(errorBuffer)[0] >= 128): #make env var
                    errorChunk = errorBuffer[slice(128), :] #make env var
                    outputBuffer = np.concatenate((outputBuffer, errorChunk), axis=0)
                    errorBuffer = np.delete(errorBuffer,slice(128), 0)
                """
            
            btserver.close_connection(self.client_socket, self.server_socket)
        except Exception as e:
            self.onError.send(e)
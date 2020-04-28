import sys
import os
import threading
import logging

import pickle
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
        self.inputSignals = [signal('anc_error_data')]
        self.outputSignal = signal('anc_output_data')

        #initialize all the signals to be in one data object
        for inputSignal in self.inputSignals:
            inputSignal.connect(self.addInputSignal)
  
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

    def addInputSignal(self, data):
        self.outputSignal.send(data)

    def run(self):
        try:
            self.server_socket = btserver.configure_server()
            self.client_socket = btserver.wait_on_client_connection(self.server_socket)

            if(self.client_socket is not None):
                self.ancError.start() #the data is moved from error to output in the ancError module
                self.ancOutput.start()

            while True:
                #check and see if the thread has been killed
                if(self.stopped()):
                    self.cleanup()
                    self.ancError.cleanup()
                    self.ancOutput.cleanup()
                    return

                [[1,2,3,4
                5,6,7,8]]


                0x0001,0x0001,0x0001,0x0001,0x0001,0x0001,0x0001,0x0001

                converted to byte data
                sends it over the wire

                how do you know when you have the right size of packet(s) to stop listening

                sizeof(numpy array)

                packet = self.client_socket.recv(1024) #make an env var

                continous byte buffer as well
                nparray = pickle.loads(packet)
                pi

                recieve data from bluetooth and put in buffer - reference mic
                receive data from error microphone and put in buffer - error mic
                receive data from target file and put in buffer - target signal

                ...[asdfadfdsafasdf]...
                ...[asdfadfdsafasdf]...
                ...[asdfadfdsafasdf]...


                run the algorithm
                
                send the data to output buffer

                if not packet: 
                    break
                
                self.referenceBuffer.append(packet)
                logging.debug(f'Receiving data from the anc client. Size is : {sys.getsizeof(packet)}')

                #refactor to integrate with the error and output thread via blinker signals
                #if(np.shape(self.ancError.errorBuffer)[0] > 0):
                #    self.ancOutput.outputBuffer = np.append(self.ancOutput.outputBuffer, self.ancError.errorBuffer, axis = 0)
                #    self.ancError.errorBuffer = np.arange(2).reshape(1,2)

                self.ancError.join(0.0)
                if self.ancError.stopped():
                    break

                self.ancOutput.join(0.0)
                if self.ancOutput.stopped():
                    break
            
            self.cleanup()
        except Exception as e:
            self.onError.send(e)
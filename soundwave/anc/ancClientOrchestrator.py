import sys
import os
import threading
import logging

import pickle
import numpy as np
from blinker import signal

from soundwave.anc.ancInput import AncInput
from soundwave.anc.ancBluetoothClient import AncBluetoothClient

class AncClientOrchestrator(threading.Thread):
    def __init__(self, device, threadName):
        threading.Thread.__init__(self, name=threadName, daemon=True)
        logging.debug('Initialize Client Orchestration thread')

        #Signals
        self.onError = signal('anc_client_orchestrator_errors')
        self.onInputData = signal('anc_input_data')
        self.onInputData.connect(self.listenForInput)
        self.onOutputData = signal('anc_btclient_data')

        #ANC algorithm information
        self.device = device

        #Thread Management
        self.threads = [AncInput(device, 'anc-reference-microphone'), AncBluetoothClient('anc-btclient')]
        self._stop = threading.Event()
  
    def stop(self): 
        logging.debug('Stopping Client Orchestration thread')
        self._stop.set()
        for thread in self.threads:
            thread.stop()
  
    def stopped(self): 
        return self._stop.isSet()
    
    def cleanup(self):
        logging.debug('Cleaning up Client Orchestration thread')
        for thread in self.threads:
            thread.cleanup()

    def listenForInput(self, data):
        logging.debug(f'Receiving data from Input Microphone thread:')
        logging.debug(data)
        self.onOutputData.send(data)

    def run(self):
        try:
            logging.debug('Running Client Orchestration thread')
            for thread in self.threads:
                thread.start()

            while True:
                #check and see if the thread has been killed
                if(self.stopped()):
                    self.cleanup()
                    return

                #check to see if any of the threads have stopped. If so, kill the orchestrator
                for thread in self.threads:
                    thread.join(0.0)
                    if thread.stopped():
                        self.stop()

        except Exception as e:
            self.onError.send(e)
            self.cleanup()
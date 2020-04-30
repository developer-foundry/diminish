import sys
import os
import threading
import logging

import pickle
import numpy as np
from blinker import signal

from soundwave.anc.ancInput import AncInput
from soundwave.anc.ancOutput import AncOutput
from soundwave.anc.ancBluetoothServer import AncBluetoothServer


class AncServerOrchestrator(threading.Thread):
    def __init__(self, device, algorithm, targetFile, threadName):
        threading.Thread.__init__(self, name=threadName, daemon=True)
        logging.debug('Initialize Server Orchestration thread')

        # Signals
        self.onError = signal('anc_server_orchestrator_errors')
        self.onReady = signal('anc_ready')
        self.onInputData = signal('anc_input_data')
        self.onOutputData = signal('anc_output_data')
        self.onInputData.connect(self.listenForErrorMicrophoneInput)

        # ANC algorithm information
        self.device = device
        self.algorithm = algorithm
        self.targetFile = targetFile

        # Continuous Buffers
        self.errorMicrophoneBuffer = np.zeros((0, 2))

        # Thread Management
        self.threads = [AncInput(device, 'anc-error-microphone'), AncOutput(device, 'anc-output-speaker'),
                        AncBluetoothServer('anc-btserver')]
        self._stop = threading.Event()

    def stop(self):
        logging.debug('Stopping Server Orchestration thread')
        self._stop.set()
        for thread in self.threads:
            thread.stop()

    def stopped(self):
        return self._stop.isSet()

    def cleanup(self):
        logging.debug('Cleaning up Server Orchestration thread')
        for thread in self.threads:
            thread.cleanup()

    def listenForErrorMicrophoneInput(self, data):
        logging.debug(f'Receiving data from Error Microphone thread:')
        logging.debug(f'Shape of data in error listener = {data.shape}')
        self.errorMicrophoneBuffer = np.concatenate((
            self.errorMicrophoneBuffer, data), axis=0)
        self.onOutputData.send(self.errorMicrophoneBuffer)

    def ancReady(self):
        return self.errorMicrophoneBuffer.shape[0] >= 5000

    def run(self):
        try:
            logging.debug('Running Server Orchestration thread')
            for thread in self.threads:
                thread.start()

            while True:
                # check and see if the thread has been killed
                if(self.stopped()):
                    self.cleanup()
                    return

                # check to see if any of the threads have stopped. If so, kill the orchestrator
                for thread in self.threads:
                    thread.join(0.0)
                    if thread.stopped():
                        self.stop()

                if self.ancReady():
                    self.onReady.send(True)

        except Exception as e:
            self.onError.send(e)
            self.cleanup()

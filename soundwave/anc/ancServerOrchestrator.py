import sys
import logging

from soundwave.anc.ancInput import AncInput
from soundwave.anc.ancOutput import AncOutput
from soundwave.anc.ancBluetoothServer import AncBluetoothServer
from soundwave.common.continuousBuffer import ContinuousBuffer

class AncServerOrchestrator():
    def __init__(self, device, algorithm, targetFile, waitSize, stepSize):
        logging.debug('Initialize Server Orchestration')
        self.device = device
        self.algorithm = algorithm
        self.targetFile = targetFile
        self.errorBuffer = ContinuousBuffer(waitSize, stepSize)
        self.outputBuffer = ContinuousBuffer(stepSize, stepSize) #output buffer does not need to wait until 'waitSize' is reached

        self.threads = [AncInput(device, self.errorBuffer, 'anc-error-microphone'),
                        AncOutput(device, self.outputBuffer, 'anc-output-speaker'),
                        AncBluetoothServer('anc-btserver')]

    def run_algorithm(self):
        data = self.errorBuffer.pop()
        self.outputBuffer.push(data)

    def run(self):
        try:
            logging.debug('Running Server Orchestration')

            for thread in self.threads:
                thread.start()
            
            # will ensure the main thread is paused until ctrl + c
            while True:
                if self.errorBuffer.is_ready():
                    self.run_algorithm()

        except Exception as e:
            logging.error(f'Exception thrown: {e}')

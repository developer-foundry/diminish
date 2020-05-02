import sys
import logging
import threading

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
        self.outputBuffer = ContinuousBuffer(0, stepSize) #output buffer does not need to wait for a waitSize; just start playing as soon as you have a big enough step
        self.ancWaitCondition = threading.Condition()
        self.threads = [AncInput(device, self.errorBuffer, stepSize, 'anc-error-microphone'),
                        AncOutput(device, self.outputBuffer, stepSize, self.ancWaitCondition, 'anc-output-speaker'),
                        AncBluetoothServer('anc-btserver')]

    def run_algorithm(self):
        data = self.errorBuffer.pop()
        self.outputBuffer.push(data)

    def is_ready(self):
        return self.errorBuffer.is_ready()

    def run(self):
        try:
            logging.debug('Running Server Orchestration')

            for thread in self.threads:
                thread.start()
            
            #loop until algorithm is ready to start
            while not self.is_ready():
                pass

            with self.ancWaitCondition:
                self.ancWaitCondition.notifyAll()

            # will ensure the main thread is paused until ctrl + c
            while True:
                self.run_algorithm()

        except Exception as e:
            logging.error(f'Exception thrown: {e}')

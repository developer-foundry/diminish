import sys
import logging
import threading

from soundwave.anc.ancInput import AncInput
from soundwave.anc.ancTarget import AncTarget
from soundwave.anc.ancOutput import AncOutput
from soundwave.anc.ancBluetoothServer import AncBluetoothServer
from soundwave.common.continuousBuffer import ContinuousBuffer
from soundwave.common.fifoBuffer import FifoBuffer
from soundwave.algorithms.signal_processing import process_signal

class AncServerOrchestrator():
    def __init__(self, device, algorithm, targetFile, waitSize, stepSize):
        logging.debug('Initialize Server Orchestration')
        self.algorithm = algorithm
        self.errorBuffer = FifoBuffer('error', waitSize, stepSize)
        self.outputBuffer = FifoBuffer('output', 0, stepSize) #output buffer does not need to wait for a waitSize; just start playing as soon as you have a big enough step
        self.targetBuffer = ContinuousBuffer('target', stepSize)
        self.ancWaitCondition = threading.Condition()
        self.threads = [AncInput(device, self.errorBuffer, stepSize, 'anc-error-microphone'),
                        AncTarget(targetFile, self.targetBuffer, stepSize, 'anc-target-file'),
                        AncOutput(device, self.outputBuffer, stepSize, self.ancWaitCondition, 'anc-output-speaker'),
                        AncBluetoothServer('anc-btserver')]

    def run_algorithm(self):
        errorSignal = self.errorBuffer.pop()
        targetSignal = self.targetBuffer.pop()
        #outputSignal, outputErrors  = process_signal(errorSignal, targetSignal, self.algorithm)
        self.outputBuffer.push(targetSignal)

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

import sys
import logging
import threading
import numpy as np

from soundwave.anc.ancInput import AncInput
from soundwave.anc.ancTarget import AncTarget
from soundwave.anc.ancOutput import AncOutput
from soundwave.anc.ancPlot import AncPlot
from soundwave.anc.ancNetworkServer import AncNetworkServer
from soundwave.common.continuousBuffer import ContinuousBuffer
from soundwave.common.fifoBuffer import FifoBuffer
from soundwave.algorithms.signal_processing import process_signal

class AncServerOrchestrator():
    def __init__(self, device, algorithm, targetFile, waitSize, stepSize, size):
        logging.debug('Initialize Server Orchestration')
        self.algorithm = algorithm
        self.errorBuffer = FifoBuffer('error', waitSize, stepSize)
        self.outputBuffer = FifoBuffer('output', waitSize, stepSize)
        self.outputErrorBuffer = FifoBuffer('output-error', 0, stepSize)
        self.referenceBuffer = FifoBuffer('reference', 0, stepSize)
        self.targetBuffer = ContinuousBuffer('target', stepSize)

        self.ancWaitCondition = threading.Condition()
        self.threads = [AncInput(device, self.errorBuffer, stepSize, 'anc-error-microphone'),
                        AncTarget(targetFile, self.targetBuffer, stepSize, size, 'anc-target-file'),
                        AncOutput(device, self.outputBuffer, stepSize, self.ancWaitCondition, 'anc-output-speaker'),
                        AncNetworkServer(self.referenceBuffer, 'anc-networkserver')]
        self.ancPlot = None

    def run_algorithm(self):
        referenceSignal = self.referenceBuffer.pop()

        # referenceCombinedWithError = np.concatenate((errorSignal, referenceSignal), axis=1)
        # outputSignal, outputErrors  = process_signal(referenceCombinedWithError, targetSignal, self.algorithm)
        # logging.info(f'outputSignal: {outputSignal.shape}')
        # self.outputBuffer.push(outputSignal)
        #if referenceSignal.shape[0] > 0:
        if referenceSignal.shape[0] == 1024:
            errorSignal = self.errorBuffer.pop()
            targetSignal = self.targetBuffer.pop()
            logging.info(f'pushing sound: {referenceSignal.shape}:{targetSignal.shape}')
            self.outputBuffer.push(referenceSignal)

        #for tracking the output error buffer we just need to push and pop
        #so that the plot subscriber picks it up
        # self.outputErrorBuffer.push(outputErrors)
        # self.outputErrorBuffer.pop()

    def is_ready(self):
        return self.errorBuffer.is_ready() and \
               self.outputBuffer.is_ready() and \
               self.referenceBuffer.is_ready()

    def run(self):
        try:
            logging.debug('Running Server Orchestration')

            for thread in self.threads:
                thread.start()
            
            #loop until algorithm is ready to start
            while not self.is_ready():
                pass

            self.ancPlot = AncPlot([self.errorBuffer, self.outputBuffer, self.targetBuffer, self.outputErrorBuffer])

            with self.ancWaitCondition:
                self.ancWaitCondition.notifyAll()

            # will ensure the main thread is paused until ctrl + c
            while True:
                if self.is_ready(): #have to keep checking as the buffer gets popped
                    self.run_algorithm()

        except Exception as e:
            logging.error(f'Exception thrown: {e}')

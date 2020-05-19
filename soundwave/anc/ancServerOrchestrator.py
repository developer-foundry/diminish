import sys
import logging
import threading
import signal
import numpy as np
import os

from soundwave.anc.ancInput import AncInput
from soundwave.anc.ancTarget import AncTarget
from soundwave.anc.ancOutput import AncOutput
from soundwave.anc.ancNetworkServer import AncNetworkServer
from common.continuousBuffer import ContinuousBuffer
from common.fifoBuffer import FifoBuffer
from soundwave.anc.ancMediator import AncMediator
from soundwave.algorithms.signal_processing import process_signal

class AncServerOrchestrator():
    def __init__(self, device, algorithm, targetFile, waitSize, stepSize, size, tuiConnection):
        logging.debug('Initialize Server Orchestration')
        self.algorithm = algorithm
        self.errorBuffer = FifoBuffer('error', 0, stepSize)
        self.outputBuffer = FifoBuffer('output', waitSize, stepSize)
        self.outputErrorBuffer = FifoBuffer('output-error', 0, stepSize)
        self.referenceBuffer = FifoBuffer('reference', 0, stepSize)
        self.targetBuffer = ContinuousBuffer('target', stepSize)

        self.tuiConnection = tuiConnection
        self.ancWaitCondition = threading.Condition()
        self.networkThread = AncNetworkServer(self.referenceBuffer, 'anc-networkserver')
        self.threads = [AncInput(device, self.errorBuffer, stepSize, 'anc-error-microphone'),
                        AncTarget(targetFile, self.targetBuffer, stepSize, size, 'anc-target-file'),
                        AncOutput(device, self.outputBuffer, stepSize, self.ancWaitCondition, 'anc-output-speaker'),
                       ]

        self.ancMediator = None
        self.paused = False
        self.paused = not (os.getenv('RUNALGO') == "TRUE")
        signal.signal(signal.SIGUSR1, self.pauseHandler)

    def pauseHandler(self, signum, frame):
        logging.debug('Toggling pause')
        self.paused = not self.paused

    def stop(self):
        for thread in self.threads:
            thread.stop()

        self.ancMediator.close_connection()
        self.ancMediator.plot_buffers(self.algorithm)

    def run_algorithm(self):
        referenceSignal = self.referenceBuffer.pop()
        errorSignal = self.errorBuffer.pop()
        targetSignal = self.targetBuffer.pop()
        referenceCombinedWithError = np.add(errorSignal, referenceSignal)

        if not self.paused:
            outputSignal, outputErrors  = process_signal(referenceCombinedWithError, targetSignal, self.algorithm)
        else:
            outputSignal = np.add(referenceSignal, targetSignal)
            outputErrors = np.subtract(targetSignal, outputSignal)

        self.outputBuffer.push(outputSignal)

        #for tracking the output error buffer we just need to push and pop
        #so that the plot subscriber picks it up
        self.outputErrorBuffer.push(outputErrors)
        self.outputErrorBuffer.pop()

    def is_ready(self):
        return self.errorBuffer.is_ready() and \
               self.referenceBuffer.is_ready()

    def run(self):
        try:
            logging.debug('Running Server Orchestration')
            self.ancMediator = AncMediator([self.errorBuffer, self.referenceBuffer, self.outputBuffer, self.targetBuffer, self.outputErrorBuffer])

            #this is a blocking call; will wait until tui connects
            if(self.tuiConnection):
                self.ancMediator.create_connection()

            self.networkThread.start()
            while not self.referenceBuffer.is_ready():
                pass

            for thread in self.threads:
                thread.start()
            
            #loop until algorithm is ready to start
            while not self.is_ready():
                pass

            with self.ancWaitCondition:
                self.ancWaitCondition.notifyAll()

            self.errorBuffer.clear()
            self.referenceBuffer.clear()
            self.outputBuffer.clear()
            self.outputErrorBuffer.clear()

            # will ensure the main thread is paused until ctrl + c
            while True:
                if self.is_ready(): #have to keep checking as the buffer gets popped
                    self.run_algorithm()

        except Exception as e:
            logging.exception(f'Exception thrown: {e}')

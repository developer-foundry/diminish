import sys
import logging
import threading
import signal
import numpy as np
import os
from pynput.keyboard import Key, Listener

from diminish.signals.inputSignal import InputSignal
from diminish.signals.targetSignal import TargetSignal
from diminish.signals.outputSignal import OutputSignal
from diminish.networking.networkServer import NetworkServer
from common.continuousBuffer import ContinuousBuffer
from common.fifoBuffer import FifoBuffer
from diminish.monitoring.monitor import Monitor
from diminish.algorithms.signal_processing import process_signal


class ServerOrchestrator():
    def __init__(self, device, algorithm, targetFile, waitSize, stepSize, size, tuiConnection):
        logging.debug('Initialize Server Orchestration')
        self.algorithm = algorithm
        self.errorBuffer = FifoBuffer('error', 0, stepSize)
        self.outputBuffer = FifoBuffer('output', waitSize, stepSize)
        self.outputErrorBuffer = FifoBuffer('output-error', 0, stepSize)
        self.referenceBuffer = FifoBuffer('reference', 0, stepSize)
        self.targetBuffer = ContinuousBuffer('target', stepSize)

        self.tuiConnection = tuiConnection
        self.waitCondition = threading.Condition()
        self.networkThread = NetworkServer(
            self.referenceBuffer, 'networkserver')
        self.threads = [InputSignal(device, self.errorBuffer, stepSize, 'error-microphone'),
                        TargetSignal(targetFile, self.targetBuffer,
                                     stepSize, size, 'target-file'),
                        OutputSignal(device, self.outputBuffer, stepSize,
                                     self.waitCondition, 'output-speaker'),
                        ]

        self.monitor = None
        self.paused = False
        signal.signal(signal.SIGUSR1, self.pauseHandler)

    def pauseHandler(self, signum, frame):
        logging.debug('Toggling pause')
        self.paused = not self.paused

    def stop(self):
        for thread in self.threads:
            thread.stop()

        self.monitor.close_connection()
        self.monitor.plot_buffers(self.algorithm)

    def run_algorithm(self):
        referenceSignal = self.referenceBuffer.pop()
        errorSignal = self.errorBuffer.pop()
        targetSignal = self.targetBuffer.pop()
        referenceCombinedWithError = np.add(errorSignal, referenceSignal)

        if not self.paused:
            outputSignal, outputErrors = process_signal(
                referenceCombinedWithError, targetSignal, self.algorithm)
        else:
            outputSignal = np.add(referenceSignal, targetSignal)
            outputErrors = np.subtract(targetSignal, outputSignal)

        self.outputBuffer.push(outputSignal)

        # for tracking the output error buffer we just need to push and pop
        # so that the plot subscriber picks it up
        self.outputErrorBuffer.push(outputErrors)
        self.outputErrorBuffer.pop()

    def is_ready(self):
        return self.errorBuffer.is_ready() and \
            self.referenceBuffer.is_ready()

    def on_release(self, key):
        if not self.tuiConnection and hasattr(key, 'char') and key.char == ('p'):
            logging.info(f'Algorithm is {"On" if self.paused else "Off"}')
            self.pauseHandler(None, None)

    def clear_buffers(self):
        self.errorBuffer.clear()
        self.referenceBuffer.clear()
        self.outputBuffer.clear()
        self.outputErrorBuffer.clear()

    def run(self):
        try:
            logging.debug('Running Server Orchestration')

            with Listener(on_release=self.on_release):
                self.monitor = Monitor(
                    [self.errorBuffer, self.referenceBuffer, self.outputBuffer, self.targetBuffer, self.outputErrorBuffer])

                # this is a blocking call; will wait until tui connects
                if(self.tuiConnection):
                    self.monitor.create_connection()

                self.networkThread.start()
                while not self.referenceBuffer.is_ready():
                    pass

                for thread in self.threads:
                    thread.start()

                # loop until algorithm is ready to start
                while not self.is_ready():
                    pass

                with self.waitCondition:
                    self.waitCondition.notifyAll()

                self.clear_buffers()

                # will ensure the main thread is paused until ctrl + c
                while True:
                    if self.is_ready():  # have to keep checking as the buffer gets popped
                        self.run_algorithm()

        except Exception as e:
            logging.exception(f'Exception thrown: {e}')

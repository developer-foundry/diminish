import sys
import logging
import threading
import signal
import numpy as np
import os

# Note the Rasperry Pi architecture does not support
# pynput so the try/catch is necessary to prevent the
# client from crashing
try:
    from pynput.keyboard import Key, Listener
except:
    pass

from diminish.signals.inputSignal import InputSignal
from diminish.signals.targetSignal import TargetSignal
from diminish.signals.outputSignal import OutputSignal
from diminish.networking.networkServer import NetworkServer
from common.continuousBuffer import ContinuousBuffer
from common.fifoBuffer import FifoBuffer
from diminish.monitoring.monitor import Monitor
from diminish.algorithms.signal_processing import process_signal

class ServerOrchestrator():
    """
    ServerOrchestrator is the primary class the coordinates
    threads and their corresponding buffers. The server handles
    a number of functions including
        * Maintaining the error microphone buffer
        * Maintaining the output or speaker buffer
        * Receiving reference microphone data from the client
        * Reading in the target signal
        * Performing the ANC processing algorithm
        * Reporting data back to the Monitor

    Will run until the server stops or it is interrupted by
    the user. A user can pause the algorithm processing with
    the `p` keybinding. The server will continue to run and 
    process data, it will just not perform the ANC algorithm

    Attributes
    ----------
    algorithm: String
        The name of the signal processing filter currently being used
    errorBuffer: FifoBuffer
        The buffer holding error microphone data
    outputBuffer: FifoBuffer
        The buffer holding speaker data
    outputErrorBuffer: FifoBuffer
        The buffer that holds the error difference between output and target signal
    referenceBuffer: FifoBuffer
        The buffer that holds reference microphone data from the client
    targetBuffer: ContinuousBuffer
        The buffer that holds the target signal data
    tuiConnection: Boolean
        A flag indicating if the server is running under the TUI interface or the CLIN interface
    waitCondition: Condition
        A threading lock to ensure the processing only starts when threads are ready
    networkThread: NetworkServer
        The networking server that performs the receiving of the reference microphone data
    threads: list
        A list maintaing the necessary threads to support the orchestration and sending of data
    monitor: Monitor
        The data monitor that performs communication with TUI, plotting, and potentially database
    paused: Boolean
        A flag indicating if the ANC algorithm should be performed during the processing of output data
    """
    def __init__(self, device, algorithm, targetFile, waitSize, stepSize, size, tuiConnection):
        """
        Parameters
        ----------
        device: String
            A string representation of the sound device being used. 'default' is usually all that is needed
        algorithm: String
            The name of the signal processing filter currently being used
        targetFile: String
            The name of the target signal data file
        waitSize: int
            The number of signal frames that should be received before the algorithm is ready
        stepSize: int
            The number of signal frames or matrix rows used in the transfer of data to the server
        size: int
            The number of frames to read from the target signal file
        tuiConnection: Boolean
            A flag indicating if the server is running under the TUI interface or the CLIN interface
        """
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
        """
        Executed via the p keybinding to toggle the paused flag

        Parameters
        ----------
        signum: int
            A integer representing the interrupt signal
        frame: stack frame
            The stack frame from the point in the program that was interrupted by the signal

        Returns
        -------
        None

        Raises
        ------
        None
        """
        logging.debug('Toggling pause')
        self.paused = not self.paused

    def stop(self):
        """
        Executed when the application is halted. Informs the 
        monitor to close and plot the results

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        for thread in self.threads:
            thread.stop()

        self.monitor.close_connection()
        self.monitor.plot_buffers(self.algorithm)

    def run_algorithm(self):
        """
        Executed every iteration to pull data from the necessary
        buffers and generate the output signal to be pushed to the
        speaker. If the ANC algorithm is on, then this would be the
        filtered signal, otherwise it just combines the target signal
        and reference microphone signals. Note error signal is not
        included in that case since the error microphone is just listening
        for feedback reasons, not because the human ear is hearing that.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
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
        """
        Determines if the buffers are ready to start
        ANC processing

        Parameters
        ----------
        None

        Returns
        -------
        Boolean

        Raises
        ------
        None
        """
        return self.errorBuffer.is_ready() and \
            self.referenceBuffer.is_ready()

    def on_release(self, key):
        """
        Provides pause functionality for the TUI

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        if not self.tuiConnection and hasattr(key, 'char') and key.char == ('p'):
            logging.info(f'Algorithm is {"On" if self.paused else "Off"}')
            self.pauseHandler(None, None)

    def clear_buffers(self):
        """
        Resets the buffers to zero data

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.errorBuffer.clear()
        self.referenceBuffer.clear()
        self.outputBuffer.clear()
        self.outputErrorBuffer.clear()

    def run(self):
        """
        Initializes buffers, threads, and orders the timing
        of threads to ensure everything is ready to start
        ANC processing

        Runs until the server is killed or an exception is thrown

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
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

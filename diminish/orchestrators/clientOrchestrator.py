import sys
import os
import threading
import logging

import numpy as np
import time

from diminish.signals.inputSignal import InputSignal
from diminish.networking.networkClient import NetworkClient
from common.fifoBuffer import FifoBuffer


class ClientOrchestrator():
    """
    ClientOrchestrator is the primary class the coordinates
    threads and their corresponding buffers. The client
    is straightforward - it reads data from the reference
    microphone and transfers that data via the network client
    to the ANC server that does the algorithm processing.

    Will run until the server stops or it is interrupted by
    the user.

    Attributes
    ----------
    device: String
        A string representation of the sound device being used. 'default' is usually all that is needed
    referenceBuffer: FifoBuffer
        A FifoBuffer that will hold the reference microphone signal
    threads: list
        A list maintaing the necessary threads to support the orchestration and sending of data
    """
    def __init__(self, device, waitSize, stepSize):
        """
        Parameters
        ----------
        device: String
            A string representation of the sound device being used. 'default' is usually all that is needed
        waitSize: int
            The number of signal frames that should be received before the algorithm is ready
        stepSize: int
            The number of signal frames or matrix rows used in the transfer of data to the server
        """
        logging.debug('Initialize Client Orchestration thread')
        self.device = device
        self.referenceBuffer = FifoBuffer('reference', 0, stepSize)
        self.threads = [InputSignal(device, self.referenceBuffer, stepSize, 'reference-microphone'),
                        NetworkClient(self.referenceBuffer, 'networkclient')]

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
            logging.debug('Running Client Orchestration thread')

            for thread in self.threads:
                thread.start()

            # will ensure the main thread is paused until ctrl + c
            while True:
                time.sleep(1)  # time takes up less cpu cycles than 'pass'

        except Exception as e:
            logging.exception(f'Exception thrown: {e}')

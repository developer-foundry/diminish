import sys
import os
import threading
import logging

import numpy as np
import time

from soundwave.signals.inputSignal import InputSignal
from soundwave.networking.networkClient import NetworkClient
from common.fifoBuffer import FifoBuffer


class ClientOrchestrator():
    def __init__(self, device, waitSize, stepSize):
        logging.debug('Initialize Client Orchestration thread')
        self.device = device
        self.referenceBuffer = FifoBuffer('reference', 0, stepSize)
        self.threads = [InputSignal(device, self.referenceBuffer, stepSize, 'reference-microphone'),
                        NetworkClient(self.referenceBuffer, 'networkclient')]

    def run(self):
        try:
            logging.debug('Running Client Orchestration thread')

            for thread in self.threads:
                thread.start()

            # will ensure the main thread is paused until ctrl + c
            while True:
                time.sleep(1)  # time takes up less cpu cycles than 'pass'

        except Exception as e:
            logging.exception(f'Exception thrown: {e}')

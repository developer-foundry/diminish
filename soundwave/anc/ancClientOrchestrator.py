import sys
import os
import threading
import logging

import numpy as np

from soundwave.anc.ancInput import AncInput
from soundwave.anc.ancNetworkClient import AncNetworkClient
from soundwave.common.fifoBuffer import FifoBuffer

class AncClientOrchestrator():
    def __init__(self, device, waitSize, stepSize):
        logging.debug('Initialize Client Orchestration thread')
        self.device = device
        self.referenceBuffer = FifoBuffer('reference', waitSize, stepSize)
        self.threads = [AncInput(device, self.referenceBuffer, stepSize, 'anc-reference-microphone'), 
                        AncNetworkClient(self.referenceBuffer, 'anc-networkclient')]

    def run(self):
        try:
            logging.debug('Running Client Orchestration thread')

            for thread in self.threads:
                thread.start()

            # will ensure the main thread is paused until ctrl + c
            while True:
                input()

        except Exception as e:
            logging.error(f'Exception thrown: {e}')

import sys
import os
import threading
import logging

import pickle
import numpy as np

from soundwave.anc.ancInput import AncInput
from soundwave.anc.ancBluetoothClient import AncBluetoothClient
from soundwave.common.continuousBuffer import ContinuousBuffer

class AncClientOrchestrator():
    def __init__(self, device, waitSize, stepSize):
        logging.debug('Initialize Client Orchestration thread')
        self.device = device
        self.referenceBuffer = ContinuousBuffer(waitSize, stepSize)
        self.threads = [AncInput(device, self.referenceBuffer, 'anc-reference-microphone'), 
                        AncBluetoothClient(self.referenceBuffer, 'anc-btclient')]

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

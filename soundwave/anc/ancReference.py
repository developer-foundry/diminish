import sys
import pickle
import threading
import logging

import numpy as np
from blinker import signal

import soundwave.bluetoothnetwork.client as btclient
import sounddevice as sd


class AncReference(threading.Thread):
    def __init__(self, device, threadName):
        threading.Thread.__init__(self, name=threadName)
        self.onError = signal('anc_reference_errors')
        self.device = device

    def listener(self, indata, frames, time, status):
        logging.debug(f'The reference microphone is processing data in the shape: {indata.shape[0]} {indata.shape[1]}')
        reference_data = pickle.dumps(indata)
        btclient.send_data(self.clientSocket, reference_data)
        logging.debug('The reference microphone has received an ack from the bluetooth server.')

    def run(self):
        try:
            self.clientSocket = btclient.configure_client()

            if(self.clientSocket is None):
                raise Exception('The anc client could not establish connection to anc server.')

            with sd.InputStream(device=(self.device, self.device),
                        blocksize=128,
                        channels=2,
                        callback=self.listener):
                input()
            
            btclient.close_connection(self.clientSocket)
        except Exception as e:
            self.onError.send(e)
import sys
import pickle
import threading

import numpy as np
from blinker import signal

import soundwave.bluetoothnetwork.client as btclient
import sounddevice as sd


class AncClient(threading.Thread):
    def __init__(self, device):
        threading.Thread.__init__(self)
        self.onError = signal('anc_client_errors')
        self.device = device

    def listener(self, indata, frames, time, status):
        print('shape: ', indata.shape)
        reference_data = pickle.dumps(indata)
        print('size of ref_data:', sys.getsizeof(reference_data))
        btclient.send_data(self.clientSocket, reference_data)
        print('ACK')

    def run(self):
        try:
            self.clientSocket = btclient.configure_client()
            raise ValueError('this is a test')
            with sd.InputStream(device=(self.device, self.device),
                        blocksize=128,
                        channels=2,
                        callback=self.listener):
                input()
            
            btclient.close_connection(self.clientSocket)
        except Exception as e:
            print('here') 
            self.onError.send(e)
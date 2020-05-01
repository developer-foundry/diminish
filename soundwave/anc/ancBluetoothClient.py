import sys
import threading
import logging
import pickle

from blinker import signal

import soundwave.bluetoothnetwork.client as btclient


class AncBluetoothClient(threading.Thread):
    def __init__(self, threadName):
        threading.Thread.__init__(self, name=threadName, daemon=True)
        logging.debug('Initialize Bluetooth Client thread')
        self.onData = signal('anc_btclient_data')
        self.onData.connect(self.listenForInput)
        self._stop = threading.Event()
        self.client_socket = None

    def stop(self):
        logging.debug('Stopping Bluetooth Client thread')
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def cleanup(self):
        logging.debug('Cleaning up Bluetooth Client thread')
        if self.client_socket is not None:
            btclient.close_connection(self.client_socket)

    def listenForInput(self, data):
        if self.client_socket is not None:
            logging.debug(f'Receiving data from Client Orchestration thread:')
            logging.debug(data)
            reference_data = pickle.dumps(data)
            btclient.send_data(self.client_socket, reference_data)

    def run(self):
        try:
            logging.debug('Running Bluetooth Client thread')
            self.client_socket = btclient.configure_client()

            if(self.client_socket is None):
                logging.error(
                    'No Bluetooth Connection was established. Bluetooth Client thread closing.')
                self.stop()
                self.cleanup()
                return

            while True:
                logging.debug('Bluetooth Client sending packets.')

                if(self.stopped()):
                    self.cleanup()
                    return

            logging.debug(
                'No more packets to send from Bluetooth Client. Bluetooth Client shutting down')
            self.stop()
            self.cleanup()
        except Exception as e:
            logging.error(f'Exception thrown: {e}')

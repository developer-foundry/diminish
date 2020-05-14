import sys
import threading
import logging
import pickle

import soundwave.bluetoothnetwork.client as btclient


class AncBluetoothClient(threading.Thread):
    def __init__(self, buffer, threadName):
        threading.Thread.__init__(self, name=threadName, daemon=True)
        logging.debug('Initialize Bluetooth Client thread')
        self.buffer = buffer
        self.client_socket = None

    def cleanup(self):
        logging.debug('Cleaning up Bluetooth Client thread')
        if self.client_socket is not None:
            btclient.close_connection(self.client_socket)

    def send_data(self):
        if self.client_socket is not None:
            logging.debug('Bluetooth Client sending packets.')
            dataToSend = self.buffer.pop()
            btclient.send_data(self.client_socket, dataToSend)

    def run(self):
        try:
            logging.debug('Running Bluetooth Client thread')
            self.client_socket = btclient.configure_client()

            if(self.client_socket is None):
                logging.error(
                    'No Bluetooth Connection was established. Bluetooth Client thread closing.')
                return

            while True:
                self.send_data()

            logging.debug(
                'No more packets to send from Bluetooth Client. Bluetooth Client shutting down')
            self.cleanup()
        except Exception as e:
            logging.exception(f'Exception thrown: {e}')
            self.cleanup()

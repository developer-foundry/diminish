import sys
import threading
import logging

import soundwave.bluetoothnetwork.server as btserver


class AncBluetoothServer(threading.Thread):
    def __init__(self, threadName):
        logging.debug('Initialize Bluetooth Server thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.server_socket = None
        self.client_socket = None

    def cleanup(self):
        logging.debug('Cleaning up Bluetooth Server thread')
        btserver.close_connection(self.client_socket, self.server_socket)

    def run(self):
        try:
            logging.debug('Running Bluetooth Server thread')
            self.server_socket = btserver.configure_server()
            self.client_socket = btserver.wait_on_client_connection(
                self.server_socket)

            if(self.client_socket is None):
                logging.error(
                    'No Bluetooth Connection was established. Bluetooth Server thread closing.')
                self.cleanup()
                return

            while True:
                arr = btserver.recv(self.client_socket)
                logging.info(f'Received arr with shape {arr.shape}')
                logging.info(f'arr: {arr[0][0]}, {arr[0][1]}')

            self.cleanup()
        except Exception as e:
            logging.exception(f'Exception thrown: {e}')
            self.cleanup()

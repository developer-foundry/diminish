import sys
import threading
import logging
import soundwave.networking.client as client

class AncNetworkClient(threading.Thread):
    def __init__(self, buffer, threadName):
        threading.Thread.__init__(self, name=threadName, daemon=True)
        logging.debug('Initialize Network Client thread')
        self.buffer = buffer
        self.client_socket = None

    def cleanup(self):
        logging.debug('Cleaning up Network Client thread')
        if self.client_socket is not None:
            client.close_connection(self.client_socket)

    def send_data(self):
        if self.client_socket is not None:
            logging.debug('Network Client sending packets.')
            dataToSend = self.buffer.pop()
            if (len(dataToSend) > 0):
                client.send_data(self.client_socket, dataToSend)

    def run(self):
        try:
            logging.debug('Running Network Client thread')
            self.client_socket = client.configure_client()

            if(self.client_socket is None):
                logging.error(
                    'No Client Connection was established. Network Client thread closing.')
                return

            while True:
                self.send_data()

            logging.debug(
                'No more packets to send from Network Client. Network Client shutting down')
            self.cleanup()
        except Exception as e:
            logging.error(f'Exception thrown: {e}')
            self.cleanup()

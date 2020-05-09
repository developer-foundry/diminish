
import sys
import threading
import logging
import soundwave.networking.server as server


class AncNetworkServer(threading.Thread):
    def __init__(self, buffer, threadName):
        logging.debug('Initialize Network Server thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.server_socket = None
        self.client_socket = None
        self.buffer = buffer

    def cleanup(self):
        logging.debug('Cleaning up Network Server thread')
        server.close_connection(self.client_socket, self.server_socket)

    def run(self):
        try:
            logging.debug('Running Network Server thread')
            self.server_socket = server.configure_server()
            self.client_socket = server.wait_on_client_connection(
                self.server_socket)

            if(self.client_socket is None):
                logging.error(
                    'No Network Connection was established. Network Server thread closing.')
                self.cleanup()
                return

            while True:
                wave = server.recv(self.client_socket)
                self.buffer.push(wave)

            self.cleanup()
        except Exception as e:
            logging.error(f'Exception thrown: {e}')
            self.cleanup()

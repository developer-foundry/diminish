import sys
import threading
import logging

from blinker import signal

import soundwave.bluetoothnetwork.server as btserver

class AncBluetoothServer(threading.Thread):
    def __init__(self, threadName):
        threading.Thread.__init__(self, name=threadName, daemon=True)
        logging.debug('Initialize Bluetooth Server thread')
        self.onError = signal('anc_btserver_errors')
        self._stop = threading.Event()
        self.server_socket = None
        self.client_socket = None
  
    def stop(self): 
        logging.debug('Stopping Bluetooth Server thread')
        self._stop.set()
  
    def stopped(self): 
        return self._stop.isSet()
    
    def cleanup(self):
        logging.debug('Cleaning up Bluetooth Server thread')
        btserver.close_connection(self.client_socket, self.server_socket)

    def run(self):
        try:
            logging.debug('Running Bluetooth Server thread')
            self.server_socket = btserver.configure_server()
            self.client_socket = btserver.wait_on_client_connection(self.server_socket)

            if(self.client_socket is not None):
                logging.error('No Bluetooth Connection was established. Bluetooth Server thread closing.')
                self.stop()
                self.cleanup()
                return
            
            while True:
                packet = self.client_socket.recv(1024) #make an env var
                if not packet: 
                    break
                else:
                    logging.debug(f'Bluetooth Server received packet from Bluetooth Client. Size is: {sys.getsizeof(packet)}')
            
            logging.debug('No more packets received from Bluetooth Client. Bluetooth Server shutting down')
            self.stop()
            self.cleanup()
        except Exception as e:
            self.onError.send(e)
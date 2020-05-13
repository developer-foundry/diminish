import sys
import threading
import logging
import ctypes
import pathlib
import os
import numpy as np

class AncNetworkClient(threading.Thread):
    def __init__(self, buffer, threadName):
        threading.Thread.__init__(self, name=threadName, daemon=True)
        logging.debug('Initialize Network Client thread')
        self.buffer = buffer

    def cleanup(self):
        logging.debug('Cleaning up Network Client thread')

    def run(self):
        try:
            logging.debug('Running Network Client thread')
            libname = pathlib.Path().absolute() / "client.so"
            c_double_p = ctypes.POINTER(ctypes.c_double)
            c_lib = ctypes.CDLL(libname)
            c_lib.send_data.argtypes = [c_double_p]

            while True:
                dataToSend = self.buffer.pop()
                if (len(dataToSend) > 0):
                    wave = dataToSend[0:len(dataToSend)]
                    waveData = wave.astype(np.float64)
                    waveToSend = waveData.ctypes.data_as(c_double_p)
                    c_lib.send_data(waveToSend)

            logging.debug(
                'No more packets to send from Network Client. Network Client shutting down')

            self.cleanup()
        except Exception as e:
            logging.error(f'Exception thrown: {e}')
            self.cleanup()

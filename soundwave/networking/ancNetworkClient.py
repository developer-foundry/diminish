import sys
import threading
import logging
import ctypes
import pathlib
import os
import numpy as np
from numpy.ctypeslib import ndpointer
import time


class AncNetworkClient(threading.Thread):
    def __init__(self, buffer, threadName):
        threading.Thread.__init__(self, name=threadName, daemon=True)
        logging.debug('Initialize Network Client thread')
        self.buffer = buffer
        self.stopped = False

    def cleanup(self):
        logging.debug('Cleaning up Network Client thread')

    def stop(self):
        self.stopped = True

    def run(self):
        try:
            logging.debug('Running Network Client thread')
            libname = pathlib.Path().absolute() / "client.so"
            c_lib = ctypes.CDLL(libname)
            c_lib.setup_connection()

            fun = c_lib.send_data
            fun.restype = None
            fun.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")]

            while not self.stopped:
                dataToSend = self.buffer.pop()
                if (len(dataToSend) > 0):
                    start = time.time()
                    fun(dataToSend)
                    end = time.time()
                    logging.debug(f'Time to send: {end - start}')

            c_lib.shutdown_connection()
            logging.debug(
                'No more packets to send from Network Client. Network Client shutting down')

            self.cleanup()
        except Exception as e:
            logging.error(f'Exception thrown: {e}')
            self.cleanup()

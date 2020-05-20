import sys
import threading
import logging
import ctypes
import pathlib
import os
import numpy as np
from numpy.ctypeslib import ndpointer
import time


class NetworkServer(threading.Thread):
    def __init__(self, buffer, threadName):
        logging.debug('Initialize Network Server thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.buffer = buffer
        self.stopped = False

    def cleanup(self):
        logging.debug('Cleaning up Network Server thread')

    def stop(self):
        self.stopped = True

    def run(self):
        try:
            logging.debug('Running Network Server thread')
            libname = pathlib.Path().absolute() / "server.so"
            c_lib = ctypes.CDLL(libname)
            STEP_SIZE = int(os.getenv("STEP_SIZE"))
            c_lib.setup_server()

            fun = c_lib.receive_message
            fun.restype = None
            fun.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                            ctypes.c_size_t,
                            ctypes.c_size_t
                            ]

            while not self.stopped:
                wave = np.zeros((STEP_SIZE, 2))
                start = time.time()
                fun(wave, STEP_SIZE, 2)
                end = time.time()
                self.buffer.push(wave)

            c_lib.shutdown_server()
            self.cleanup()
        except Exception as e:
            logging.error(f'Exception thrown: {e}')
            self.cleanup()

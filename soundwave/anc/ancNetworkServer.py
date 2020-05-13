import sys
import threading
import logging
import ctypes
import pathlib
import os

class AncNetworkServer(threading.Thread):
    def __init__(self, buffer, threadName):
        logging.debug('Initialize Network Server thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.buffer = buffer

    def cleanup(self):
        logging.debug('Cleaning up Network Server thread')

    def run(self):
        try:
            logging.debug('Running Network Server thread')
            libname = pathlib.Path().absolute() / "server.so"
            c_double_p = ctypes.POINTER(ctypes.c_double)
            c_lib = ctypes.CDLL(libname)
            c_lib.receive_message.argtypes = [c_double_p]
            STEP_SIZE = int(os.getenv("STEP_SIZE"))

            while True:
                wave = (ctypes.c_double * STEP_SIZE * 2)()
                c_lib.receive_message(wave)
                #TODO likely need to convert wave to a np array?
                self.buffer.push(wave)

            self.cleanup()
        except Exception as e:
            logging.error(f'Exception thrown: {e}')
            self.cleanup()

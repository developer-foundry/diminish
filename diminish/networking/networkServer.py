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
    """
    NetworkServer is a wrapper python class executing the external
    C library to perform the receiving of numpy matricies. It is
    used by the ServerOrchestrator directly and runs as its own
    thread.

    The network protocol is extrememly simple. Currently it expects
    STEP_SIZE rows to be transferred to the server. The C library 
    computes the number of bytes to send. STEP_SIZE must be the same
    on the server and client for this to work.

    Since it is only receiving reference microphone data the number
    of columns is hard coded at 2. Thus the number of bytes received is 
    the simply STEP_SIZE * 2 * sizeof(double). sizeof(double) is
    typically 8 bytes on the architectures being used.

    Attributes
    ----------
    buffer : FiFoBuffer
        A thread-safe FifoBuffer that writes the underlying data stream (stereo sound)
    stopped: Boolean
        A flag indicating if the algorithm is running
    """
    def __init__(self, buffer, threadName):
        """
        Parameters
        ----------
        buffer: FiFoBuffer
            A thread-safe FifoBuffer that reads the underlying data stream (stereo sound)
        threadName : str
            The name of the thread. Utilized for debugging.
        """
        logging.debug('Initialize Network Server thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.buffer = buffer
        self.stopped = False

    def cleanup(self):
        """
        Cleans up any necessary attributes when the thread is stopped

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        logging.debug('Cleaning up Network Server thread')

    def stop(self):
        """
        Called when the algorithm is stopped and sets the stopped flag to False

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.stopped = True

    def run(self):
        """
        The primary function of this class executed by ServerOrchestrator.
        Loads the external C library, starts up the network client, recevies 
        the reference microphone data, and closes the network connection.

        This will run as long as the stopped flag is not False

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
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
                fun(wave, STEP_SIZE, 2)
                self.buffer.push(wave)

            c_lib.shutdown_server()
            self.cleanup()
        except Exception as e:
            logging.error(f'Exception thrown: {e}')
            self.cleanup()

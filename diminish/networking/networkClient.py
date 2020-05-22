import sys
import threading
import logging
import ctypes
import pathlib
import os
import numpy as np
from numpy.ctypeslib import ndpointer
import time


class NetworkClient(threading.Thread):
    """
    NetworkClient is a wrapper python class executing the external
    C library to perform the sending of numpy matricies. It is
    used by the ClientOrchestrator directly and runs as its own
    thread.

    The network protocol is extrememly simple. Currently it expects
    STEP_SIZE rows to be transferred to the server. The C library 
    computes the number of bytes to send. STEP_SIZE must be the same
    on the server and client for this to work.

    Since it is only transferring reference microphone data the number
    of columns is hard coded at 2. Thus the number of bytes sent is 
    the simply STEP_SIZE * 2 * sizeof(double). sizeof(double) is
    typically 8 bytes on the architectures being used.

    Attributes
    ----------
    buffer : FiFoBuffer
        A thread-safe FifoBuffer that reads the underlying data stream (stereo sound)
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
        threading.Thread.__init__(self, name=threadName, daemon=True)
        logging.debug('Initialize Network Client thread')
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
        logging.debug('Cleaning up Network Client thread')

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
        The primary function of this class executed by ClientOrchestrator.
        Loads the external C library, starts up the network client, transfers
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

import sys
import threading
import logging
import os
import psutil
import numpy as np

import sounddevice as sd
from common.continuousBuffer import ContinuousBuffer
import diminish.plotting.plot as plot
import threading
from multiprocessing.connection import Listener
from common.common import guiRefreshTimer


class Monitor():
    """
    Monitor is utilized by Dimish to track the entire data set sound data for the 
    error microphone, reference microphone, target file, output speaker, and output error.

    It will also send information to subscribers like the TUI application.

    Attributes
    ----------
    buffers : threading.Lock
        A lock utilized to control access to the underlying buffer because these buffers are utilized by multiple threads.
    dataClient : Listener
        Using the multiprocessing Listener object to push data to the TUI application
    process : psutil.Process
        Used to retrieve system level monitoring information like CPU/Memory.
    """

    def __init__(self, buffers):
        """
        Parameters
        ----------
        buffers : array
            An array of buffers to monitor
        """
        self.buffers = {}  # dictionary to hold the data that is popped off buffers for ploting
        self.dataClient = None  # used by the TUI application to pass data
        self.process = psutil.Process(os.getpid())
        for buffer in buffers:
            self.buffers[buffer.name] = np.empty((0, 2))
            buffer.subscribe(self.observe)

    def observe(self, bufferName, data):
        """
        Function utilized to track the anc data over time. Monitors the real time data from the algorithm and tracks it for 
        plotting or analysis

        Parameters
        ----------
        bufferName : str
            The name of the buffer that is passing data to the monitor (error, target, etc)
        data : np.array
            An array of sound data to add to the buffer

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.buffers[bufferName] = np.concatenate(
            (self.buffers[bufferName], data), axis=0)

    def plot_buffers(self, algorithm):
        """
        Plots all buffers that have been monitored using mathplotlib

        Parameters
        ----------
        algorithm : str
            The name of the algorithm utilized in the run of the system.

        Returns
        -------
        None

        Raises
        ------
        None
        """
        logging.debug(f'Plotting buffers')
        plot.plot_vertical_buffers(algorithm, 'anc', self.buffers)

    def sendData(self):
        """
        Used to send data to the TUI application. This function runs on a timer that sends data
        every <guiRefreshTimer>

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
        for bufferName in self.buffers:
            if(len(self.buffers[bufferName]) > 0):
                self.dataClient.send(bufferName)

                if(bufferName != "output-error"):
                    self.dataClient.send(self.buffers[bufferName][-1])
                else:
                    self.dataClient.send(np.average(self.buffers[bufferName]))

        self.dataClient.send('end buffers')

        self.dataClient.send(
            self.process.memory_info().rss / 1000000)  # send in MB
        self.dataClient.send(psutil.cpu_percent())

        threading.Timer(guiRefreshTimer, self.sendData).start()

    def create_connection(self):
        """
        Creates a data connection to the TUI process in order to send data.
        Uses the python multiprocessing library to communicate between processes.

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
        self.listener = Listener(
            ('localhost', 5000), authkey=b'secret password')
        logging.debug('Connecting Server...')
        self.dataClient = self.listener.accept()
        logging.debug('Connected Server...')
        self.sendData()

    def close_connection(self):
        """
        Closes the connection to the TUI process

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
        if(self.dataClient is not None):
            self.dataClient.close()

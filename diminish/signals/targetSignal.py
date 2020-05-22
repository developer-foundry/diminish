import sys
import threading
import logging

import numpy as np

import soundfile as sf
from common.continuousBuffer import ContinuousBuffer


class TargetSignal(threading.Thread):
    """
    Represents an output signal such as the speaker
    Runs in its own thread to push data onto the buffer

    Attributes
    ----------
    buffer : ContinuousBuffer
        A thread-safe ContinuousBuffer that reads the underlying data stream (stereo sound)
    stepSize: int
        The number of signal frames or matrix rows used in the transfer of data to the server
    size: int
        The number of frames to read from the target signal file
    targetFile: String
        The name of the target signal data file
    targetSignal: numpy.ndarray
        The sound data read in from targetFile
    stopped: Boolean
        A flag indicating if the algorithm is running
    """
    def __init__(self, targetFile, buffer, stepSize, size, threadName):
        """
        Parameters
        ----------
        targetFile: String
            The name of the target signal data file
        buffer : ContinousBuffer
            A thread-safe ContinuousBUffer that reads the underlying data stream (stereo sound)
        stepSize: int
            The number of signal frames or matrix rows used in the transfer of data to the server
        size: int
            The number of frames to read from the target signal file
        threadName : str
            The name of the thread. Utilized for debugging.
        """
        logging.debug('Initialize Target File thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.buffer = buffer
        self.stepSize = stepSize
        self.size = size
        self.targetFile = targetFile
        self.targetSignal = None
        self.stopped = False

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
        The primary thread function that initializes the
        TargetStream. This is called once to load the buffer
        and then the algorithm can use the ContinuousBuffer
        to load "new" information into the algorithm

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
            # this thread does not keep running. it will end as soon as the buffer is populated
            logging.debug('Running Target File thread')
            self.targetSignal, _ = sf.read(
                self.targetFile, dtype='float32')
            self.buffer.push(self.targetSignal[0:self.size])

        except Exception as e:
            logging.exception(f'Exception thrown: {e}')

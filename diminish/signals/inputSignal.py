import sys
import threading
import logging
import time
import numpy as np

import sounddevice as sd
from common.continuousBuffer import ContinuousBuffer


class InputSignal(threading.Thread):
    """
    Represents an input signal such as the error microphone
    or reference microphone. Runs in its own thread to push
    and pop data onto the buffer

    Attributes
    ----------
    buffer : FiFoBuffer
        A thread-safe FifoBuffer that reads the underlying data stream (stereo sound)
    device: String
        A string representation of the sound device being used. 'default' is usually all that is needed
    stepSize: int
        The number of signal frames or matrix rows used in the transfer of data to the server
    stopped: Boolean
        A flag indicating if the algorithm is running
    """
    def __init__(self, device, buffer, stepSize, threadName):
        """
        Parameters
        ----------
        device: String
            A string representation of the sound device being used. 'default' is usually all that is needed
        buffer : FiFoBuffer
            A thread-safe FifoBuffer that reads the underlying data stream (stereo sound)
        stepSize: int
            The number of signal frames or matrix rows used in the transfer of data to the server
        threadName : str
            The name of the thread. Utilized for debugging.
        """
        logging.debug('Initialize Input Microphone thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.buffer = buffer
        self.device = device
        self.stepSize = stepSize
        self.stopped = False

    def listener(self, indata, frames, time, status):
        """
        Callback function for sounddevice InputStream
        Is called periodically to place data from the
        microphone and pushes data onto its respective
        buffer. This is driven by PulseAudio under the
        covers of sounddevice

        Parameters
        ----------
        indata: numpy.ndarray
            The numpy matrix that contains the microphone data with
            one column per channel
        frames: int
            The number of rows for indata
        time: CData
            Provides a CFFI structure with timestamps indicating the ADC capture time of the first sample in the input buffer
        status: CallbackFlags
            Instance indicating whether input and/or output buffers have been inserted or will be dropped to overcome underflow or overflow conditions.

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.buffer.push(indata)

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
        InputStream and continuously calls the Stream
        listener to place data onto the buffer

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
            logging.debug('Running Input Microphone thread')

            with sd.InputStream(device=self.device,
                                channels=2,
                                blocksize=self.stepSize,
                                callback=self.listener):
                while not self.stopped:
                    time.sleep(1)  # time takes up less cpu cycles than 'pass'

        except Exception as e:
            logging.exception(f'Exception thrown: {e}')

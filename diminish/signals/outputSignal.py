import sys
import threading
import logging
import time

import numpy as np
import sounddevice as sd


class OutputSignal(threading.Thread):
    """
    Represents an output signal such as the speaker
    Runs in its own thread to push data onto the buffer

    Attributes
    ----------
    device: String
        A string representation of the sound device being used. 'default' is usually all that is needed
    buffer : FiFoBuffer
        A thread-safe FifoBuffer that reads the underlying data stream (stereo sound)
    stepSize: int
        The number of signal frames or matrix rows used in the transfer of data to the server
    waitCondition: Condition
        The threading condition or lock that is used to signal when output can start
    stopped: Boolean
        A flag indicating if the algorithm is running
    """
    def __init__(self, device, buffer, stepSize, waitCondition, threadName):
        """
        Parameters
        ----------
        device: String
            A string representation of the sound device being used. 'default' is usually all that is needed
        buffer : FiFoBuffer
            A thread-safe FifoBuffer that reads the underlying data stream (stereo sound)
        stepSize: int
            The number of signal frames or matrix rows used in the transfer of data to the server
        waitCondition: Condition
            The threading condition or lock that is used to signal when output can start
        threadName : str
            The name of the thread. Utilized for debugging.
        """
        logging.debug('Initializing Output Speaker thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.device = device
        self.buffer = buffer
        self.stepSize = stepSize
        self.waitCondition = waitCondition
        self.stopped = False

    def listener(self, outdata, frames, time, status):
        """
        Callback function for sounddevice OutputStream
        Is called periodically to place data from the
        buffer into the speaker output This is driven 
        by PulseAudio under the covers of sounddevice

        Parameters
        ----------
        outdata: numpy.ndarray
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
        data = self.buffer.pop()
        size = data.shape[0]
        outdata[:size] = data

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
        OutputStream and continuously calls the Stream
        listener to place data from the buffer into the
        Stream

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
            logging.debug('Running Output Speaker thread')
            with self.waitCondition:
                self.waitCondition.wait()

                with sd.OutputStream(device=self.device,
                                     channels=2,
                                     blocksize=self.stepSize,
                                     callback=self.listener):
                    while not self.stopped:
                        # time takes up less cpu cycles than 'pass'
                        time.sleep(1)

        except Exception as e:
            logging.exception(f'Exception thrown: {e}')

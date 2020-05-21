import threading
import logging
import numpy as np
from typing import Callable


class FifoBuffer():
    """
    FifoBuffer is a buffer that acts as a Queue
    Items that are popped are deleted from the buffer
    Typically a FifoBuffer is continuously pushed and popped from
    Locking is required as the pushing and popping occurs from different
    threads.

    FifoBuffer is utilized by diminish to handle the Input Signal
    and Output Signals.

    Attributes
    ----------
    lock : threading.Lock
        A lock utilized to control access to the underlying buffer because these buffers are utilized by multiple threads.
    buffer : np.array
        A numpy array that holds the underlying data stream (stereo sound)
    waitSize : int
        The starting location to utilize when data is popped. Anything before that in the buffer is not needed.
        Provides a mechanism to capture data while the algorithm is syncronizing.
    stepSize : int
        The amount of data to pop off the buffer.
    numChannels : int
        The number of channels of the sound file in question. Likely will always be 2.
    name : str
        The name of the buffer. Utilized for debugging, but also the monitoring system for graphing, database insertion, etc.
    subscriber : Callable
        Each buffer can have one subscriber that will be notified upon a pop.


    Methods
    -------
    subscribe(observer: Callable)
        Subscribes an observer to be notified upon a pop of the buffer.
    push(data: np.array)
        Adds data to the end of the buffer
    pop()
        Returns a chunk of data from the front of the buffer to 'stepSize'.
        Deletes the chunk from the buffer.
    is_ready()
        Determines whether or not the buffer is ready for processing
    size()
        Returns the size of the buffer
    clear()
        Zeros out the entire buffer.
    """

    def __init__(self, name, waitSize, stepSize, numChannels=2):
        """
        Parameters
        ----------
        name : str
            The name of the buffer. Utilized for debugging, but also the monitoring system for graphing, database insertion, etc.
        waitSize : int
            The starting location to utilize when data is popped. Anything before that in the buffer is not needed.
            Provides a mechanism to capture data while the algorithm is syncronizing.
        stepSize : int
            The amount of data to pop off the buffer.
        numChannels : int
            The number of channels of the sound file in question. Likely will always be 2.
        """
        self.lock = threading.Lock()
        self.buffer = np.zeros((0, numChannels))
        self.waitSize = waitSize
        self.stepSize = stepSize
        self.numChannels = numChannels
        self.name = name
        self.subscriber: Callable = None

    def subscribe(self, observer: Callable):
        """Subscribes an observer to be notified upon a pop of the buffer.

        Parameters
        ----------
        observer : Callable
            The observer to attach to the subscriber for notification of a pop.

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.subscriber = observer

    def push(self, data):
        """
        Adds data to the end of the buffer

        Parameters
        ----------
        data : np.array
            The numpy array data to add to the end of the buffer

        Returns
        -------
        None

        Raises
        ------
        None
        """
        with self.lock:
            self.buffer = np.concatenate((self.buffer, data), axis=0)

    def pop(self):
        """
        Returns a chunk of data from the front of the buffer to 'stepSize'.
        Deletes the chunk from the buffer.

        Parameters
        ----------
        None

        Returns
        -------
        data : np.array
            A numpy array representing a chunk of the buffer.

        Raises
        ------
        None
        """
        with self.lock:
            end = self.waitSize + self.stepSize
            dataToRemove = self.buffer[self.waitSize:end]
            self.buffer = np.delete(self.buffer, np.s_[self.waitSize:end], 0)

            # notify subscriber
            if self.subscriber is not None:
                self.subscriber(self.name, dataToRemove)
            return dataToRemove

    def is_ready(self):
        """
        Determines whether or not the buffer is ready for processing

        Parameters
        ----------
        None

        Returns
        -------
        isReady : boolean
            A boolean representing whether or not the buffer is ready for processing in the Diminish algorithm

        Raises
        ------
        None
        """
        switcher = {
            'output': lambda: True,
            'output-error': lambda: True,
            'error': lambda: self.size() >= self.stepSize,
            'reference': lambda: self.size() >= self.stepSize
        }

        func = switcher.get(self.name)
        return func()

    def size(self):
        """
        Returns the size of the buffer

        Parameters
        ----------
        None

        Returns
        -------
        size : int
            Size of the buffer

        Raises
        ------
        None
        """
        return self.buffer.shape[0]

    def clear(self):
        """
        Zeros out the entire buffer.

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
        self.buffer = np.zeros((0, self.numChannels))

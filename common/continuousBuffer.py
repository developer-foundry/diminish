import threading
import logging
import numpy as np
from typing import Callable


class ContinuousBuffer():
    """
    ContinuousBuffer is a buffer that acts as a rolling buffer
    Items that are popped are simply moved to the end of the buffer
    Typically a ContinuousBuffer is initialized with its entire data set
    up front rather than continuously pushing data onto the buffer.

    ContinuousBuffer is utilized by diminish to handle the Target File buffer.

    Attributes
    ----------
    lock : threading.Lock
        A lock utilized to control access to the underlying buffer because these buffers are utilized by multiple threads.
    buffer : np.array
        A numpy array that holds the underlying data stream (stereo sound)
    maxSize : int
        The maximum size of the buffer.
    currentLocation : int
        Tracks the current location that the buffer is at. Used by the pop method to determine the starting location of the next chunk.
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
        Returns a chunk of data from 'currentLocation' to 'currentLocation + stepSize'.
        Moves that chunk to the end of the buffer
    size()
        Returns the size of the buffer
    """

    def __init__(self, name, stepSize, numChannels=2):
        """
        Parameters
        ----------
        name : str
            The name of the buffer. Utilized for debugging, but also the monitoring system for graphing, database insertion, etc.
        stepSize : int
            The amount of data to pop off the buffer.
        numChannels : int
            The number of channels of the sound file in question. Likely will always be 2.
        """
        self.lock = threading.Lock()
        self.buffer = None
        self.maxSize = 0
        self.currentLocation = 0
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
            self.buffer = data
            self.maxSize = len(data)

    def pop(self):
        """
        Returns a chunk of data from 'currentLocation' to 'currentLocation + stepSize'.
        Moves that chunk to the end of the buffer

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
            # step size in this case represents the end of what you want to slize
            # from the continuous buffer
            end = self.currentLocation + self.stepSize
            if self.maxSize < end:
                self.currentLocation = 0
                end = self.stepSize

            dataToMove = self.buffer[self.currentLocation:end]
            self.currentLocation += self.stepSize

            # notify subscriber
            if self.subscriber is not None:
                self.subscriber(self.name, dataToMove)

            return dataToMove

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

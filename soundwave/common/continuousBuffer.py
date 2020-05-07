import threading
import logging
import numpy as np
from typing import Callable

class ContinuousBuffer():
    def __init__(self, name, stepSize, numChannels = 2):
        self.lock = threading.Lock()
        self.buffer = None
        self.maxSize = 0
        self.currentLocation = 0
        self.stepSize = stepSize
        self.numChannels = numChannels
        self.name = name #used to help with debugging
        self.subscriber:Callable = None #define a subscriber that is interested in the pop feature

    def subscribe(self, observer:Callable):
        self.subscriber = observer

    def push(self, data):
        with self.lock:
            self.buffer = data
            self.maxSize = len(data)
    
    def pop(self):
        with self.lock:
            #step size in this case represents the end of what you want to slize
            #from the continuous buffer
            end = self.currentLocation + self.stepSize
            if self.maxSize < end:
                self.currentLocation = 0

            dataToMove = self.buffer[self.currentLocation:end]
            self.buffer = np.roll(self.buffer, -self.stepSize, 0) #need to roll negative to move what is in the front to the back of the buffer

            self.currentLocation += self.stepSize

            #notify subscriber
            if self.subscriber is not None:
                self.subscriber(self.name, dataToMove)

            return dataToMove

    def size(self):
        return self.buffer.shape[0]
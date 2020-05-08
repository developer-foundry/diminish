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
                end = self.stepSize

            dataToMove = self.buffer[self.currentLocation:end]
            self.currentLocation += self.stepSize

            #notify subscriber
            if self.subscriber is not None:
                self.subscriber(self.name, dataToMove)

            return dataToMove

    def size(self):
        return self.buffer.shape[0]
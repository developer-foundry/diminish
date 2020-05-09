import threading
import logging
import numpy as np
from typing import Callable

class FifoBuffer():
    def __init__(self, name, waitSize, stepSize, numChannels = 2):
        self.lock = threading.Lock()
        self.buffer = np.zeros((0, numChannels))
        self.waitSize = waitSize
        self.stepSize = stepSize
        self.numChannels = numChannels
        self.name = name #used to help with debugging
        self.subscriber:Callable = None #define a subscriber that is interested in the pop feature

    def subscribe(self, observer:Callable):
        self.subscriber = observer

    def push(self, data):
        with self.lock:
            self.buffer = np.concatenate((self.buffer, data), axis=0)
    
    def pop(self):
        with self.lock:
            #step size in this case represents the end of what you want to slize
            #from the continuous buffer
            end = self.waitSize + self.stepSize
            dataToRemove = self.buffer[self.waitSize:end]
            self.buffer = np.delete(self.buffer, np.s_[self.waitSize:end], 0)

            #notify subscriber
            if self.subscriber is not None:
                self.subscriber(self.name, dataToRemove)
            return dataToRemove
    
    def is_ready(self):
        switcher = {
            'output': lambda: self.size() < self.waitSize*5,
            'output-error': lambda: True,
            'error': lambda: self.size() > self.waitSize + self.stepSize,
            'reference': lambda: self.size() >= self.waitSize + self.stepSize
        }

        func = switcher.get(self.name)
        return func()

    def size(self):
        return self.buffer.shape[0]
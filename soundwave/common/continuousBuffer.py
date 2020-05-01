import threading
import logging
import numpy as np

class ContinuousBuffer():
    def __init__(self, waitSize, stepSize, numChannels = 2):
        self.lock = threading.Lock()
        self.buffer = np.zeros((0, numChannels))
        self.waitSize = waitSize
        self.stepSize = stepSize

    def push(self, data):
        with self.lock:
            self.buffer = np.concatenate((self.buffer, data), axis=0)
    
    def pop(self):
        with self.lock:
            dataToRemove = self.buffer[self.waitSize::self.stepSize]
            np.delete(self.buffer, np.s_[self.waitSize::self.stepSize], 0)
            return dataToRemove
    
    def is_ready(self):
        return self.size() > self.waitSize + self.stepSize

    def size(self):
        return self.buffer.shape[0]
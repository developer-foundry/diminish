from influx.influxService import InfluxService
import datetime
import time
import sys
import threading
import logging
import os
import psutil
import numpy as np

import sounddevice as sd
from common.fifoBuffer import FifoBuffer
import threading
from multiprocessing.connection import Listener
from common.common import guiRefreshTimer

flushTimer = 5

class AncMonitor(threading.Thread):
    def __init__(self, buffers, threadName):
        logging.debug('Initializing Anc Monitor thread')
        threading.Thread.__init__(self, name=threadName, daemon=True)
        self.buffers = {} #dictionary to hold the data that is popped off buffers for ploting
        self.dataClient = None #used by the TUI application to pass data
        self.process = psutil.Process(os.getpid())
        self.influxService = InfluxService()
        self.stopped = False

        for buffer in buffers:
            self.buffers[buffer.name] = FifoBuffer(buffer.name, 0, 1024)
            buffer.subscribe(self.observe) #subscribe the real buffer to AncMonitor
        
        threading.Timer(flushTimer, self.flush).start() #setup timer to flush the monitoring buffer
    
    def stop(self):
        self.stopped = True

    def run(self):
        try:
            logging.debug('Running Anc Monitor thread')
            while not self.stopped :
                time.sleep(1) #time takes up less cpu cycles than 'pass'

        except Exception as e:
            logging.exception(f'Exception thrown: {e}')

    def flush(self):
        logging.info(f'Flushing ')
        #first check and see if the buffer has data to write
        for bufferName in self.buffers:
            if(self.buffers[bufferName].size() > 0):
                logging.info(f'Flushing {bufferName}')
                #construct a wave and clear the buffer via flush
                bufferData = self.buffers[bufferName].flush()
                waveName = 'Session - {0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
                self.influxService.addWave(waveName, bufferName, bufferData)
                logging.info(f'Completed Flushing {bufferName}')
        
        threading.Timer(flushTimer, self.flush).start()

    def observe(self, bufferName, data):
        self.buffers[bufferName].push(data)

    def notify(self):
        for bufferName in self.buffers:
            if(self.buffers[bufferName].size() > 0):
                self.dataClient.send(bufferName)

                if(bufferName != "output-error"):
                    self.dataClient.send(self.buffers[bufferName].peekLast())
                else:
                    self.dataClient.send(self.buffers[bufferName].average())

        self.dataClient.send('end buffers')

        self.dataClient.send(self.process.memory_info().rss / 1000000) #send in MB
        self.dataClient.send(psutil.cpu_percent())
        
        threading.Timer(guiRefreshTimer, self.notify).start()
        
    def create_connection(self):
        self.listener = Listener(('localhost', 5000), authkey=b'secret password')
        logging.debug('Connecting Server...')
        self.dataClient = self.listener.accept()
        logging.debug('Connected Server...')
        self.notify()

    def close_connection(self):
        if(self.dataClient is not None):
            self.dataClient.close()
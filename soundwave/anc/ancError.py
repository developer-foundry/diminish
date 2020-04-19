import sys
import pickle
import threading
import logging
from functools import partial

import numpy as np
from blinker import signal

import soundwave.bluetoothnetwork.server as btserver
import sounddevice as sd

class AncError(threading.Thread):
    def __init__(self, device, threadName):
        threading.Thread.__init__(self, name=threadName)
        self.onError = signal('anc_server_errors')
        self.device = device
        self.errorBuffer = np.arange(2).reshape(1,2)

    def listener(self, indata, frames, time, status):
        logging.debug('The error microphone is processing data in the shape: %s' % indata.shape)
        self.errorBuffer = np.concatenate((self.errorBuffer, indata), axis=0)

    def run(self):
        try:
            with sd.InputStream(device=(self.device, self.device),
                        blocksize=128,
                        channels=2,
                        callback=self.listener):
                input()
        except Exception as e:
            self.onError.send(e)

"""
def anc_output_listener(outdata, frames, time, status):
    global outputBuffer
    outputChunk = outputBuffer[slice(128), :] #make env var
    logging.debug('output chunk', outputChunk)
    if(np.shape(outputChunk)[0] == 128):
        outdata[:] = outputChunk
        outputBuffer = np.delete(outputBuffer,slice(128), 0)
    

def setup_output_stream(device):
    with sd.OutputStream(device=(device, device), 
                         blocksize=128, #make an env var
                         channels=2,
                         callback=anc_output_listener):
        input()


def setup_reference_microphone_buffer(device):
    #global referenceBuffer
    #server_socket = btserver.configure_server()
    #client_socket = btserver.wait_on_client_connection(server_socket)

    # start listening to error microphone now that connection is made
    thread.start_new_thread( setup_error_microphone_buffer, (device,) )
    thread.start_new_thread( setup_output_stream, (device,) )

    #while True:
    #    packet = client_socket.recv(1024) #make an env var
    #    if not packet: break
    #    referenceBuffer.append(packet)

    #btserver.close_connection(client_socket, server_socket)


def process_server_buffers():
    global errorBuffer
    global referenceBuffer
    global outputBuffer
    
    # output the error buffer for testing
    if(np.shape(errorBuffer)[0] >= 128): #make env var
        errorChunk = errorBuffer[slice(128), :] #make env var
        outputBuffer = np.concatenate((outputBuffer, errorChunk), axis=0)
        errorBuffer = np.delete(errorBuffer,slice(128), 0)
        # play the chunk for testing output in this mode


def anc_server(device, targetFile, algorithm):
    # setup thread for the reference microphone
    thread.start_new_thread( setup_reference_microphone_buffer, (device, ) )

    # setup an infinite loop to process the buffers simultaneously
    process_server_buffers()
    """
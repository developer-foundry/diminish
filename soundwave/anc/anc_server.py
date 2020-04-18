import sys
import pickle
from functools import partial
import soundwave.bluetoothnetwork.server as btserver
import sounddevice as sd
"""
def anc_error_microphone_listener(indata, frames, time, status):
    global errorBuffer
    errorBuffer = np.concatenate((errorBuffer, indata), axis=0)
    print('errorBuffer', errorBuffer)


def setup_error_microphone_buffer(device):
    with sd.InputStream(device=(device, device), 
                         blocksize=128, #make an env var
                         channels=2,
                         callback=anc_error_microphone_listener):
        input()

def anc_output_listener(outdata, frames, time, status):
    global outputBuffer
    outputChunk = outputBuffer[slice(128), :] #make env var
    print('output chunk', outputChunk)
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
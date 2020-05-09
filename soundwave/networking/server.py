import time
import socket
import logging
import struct
import numpy as np
import os
from soundproto import sound_pb2

from dotenv import load_dotenv
load_dotenv()

def configure_server():
    HOST = os.getenv('SERVER')
    PORT = int(os.getenv('PORT'))
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('',PORT))
    server_sock.listen(1)
    logging.info(f'Waiting for connection on socket port {PORT}')
    return server_sock

def wait_on_client_connection(server_sock):
    conn, addr = server_sock.accept()
    logging.info(f'Accepted connection from {addr}')
    return conn

def close_connection(client_sock, server_sock):
    client_sock.close()
    server_sock.close()
    logging.info('Closing bluetooth connection to client')

def socket_read_n(sock, n):
    buf = bytes()
    while n > 0:
        data = sock.recv(n)
        if data == '':
            raise RuntimeError('unexpected connection close')
        buf += data
        n -= len(data)
    return buf

def get_message(sock, msgtype):
    len_buf = socket_read_n(sock, 4)
    msg_len = struct.unpack('>L', len_buf)[0]
    msg_buf = socket_read_n(sock, msg_len)

    msg = msgtype()
    msg.ParseFromString(msg_buf)
    return msg

def recv(socket):
    start = time.time()
    soundwave = get_message(socket, sound_pb2.SoundWave)
    wave = np.empty((0,2))
    for i in soundwave.samples:
        sample_arr = np.array([[i.first, i.second]])
        wave = np.concatenate((wave, sample_arr), axis=0)

    end = time.time()
    logging.info(f'Time to recevie: {end - start}')
    return wave


import sys
import socket
import logging
import struct
import os
import numpy as np
from soundproto import sound_pb2

from dotenv import load_dotenv
load_dotenv()

def configure_client():
    HOST = os.getenv('SERVER')
    PORT = os.getenv('PORT')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        logging.info(f'Connected to server {HOST}')
        return s

def send_message(sock, message):
    s = message.SerializeToString()
    packed_len = struct.pack('>L', len(s))
    return sock.sendall(packed_len + s)

def send_data(socket, data):
    soundwave = sound_pb2.SoundWave()
    soundwave.name = "Reference"

    for x in data:
      sample = soundwave.samples.add()
      sample.first = float(x[0])
      sample.second = float(x[1])

    return send_message(socket, soundwave)

def close_connection(socket):
    socket.close()
    logging.info('Disconnected from server')
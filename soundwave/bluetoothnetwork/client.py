import sys
import bluetooth
import logging
import struct
import numpy as np
from soundproto import sound_pb2

uuid = '87f39d29-7d6d-437d-973b-fba39e49d4ee'

def configure_client():
    addr = None

    logging.info('Searching for ANC service')
    service_matches = bluetooth.find_service(uuid=uuid, address=addr)

    if len(service_matches) == 0:
        logging.info('Could not find the ANC service.')
        return

    first_match = service_matches[0]
    port = first_match['port']
    name = first_match['name']
    host = first_match['host']

    logging.info('Connecting to \'{}\' on {}'.format(name, host))

    socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    socket.connect((host, port))
    logging.info('Connected to ANC server')
    return socket

def send_message(sock, message):
    s = message.SerializeToString()
    packed_len = struct.pack('>L', len(s))
    return sock.send(packed_len + s)

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
    logging.info('Disconnected.')
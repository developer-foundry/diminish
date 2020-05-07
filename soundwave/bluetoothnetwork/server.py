import bluetooth
import logging
import struct
import numpy as np
from soundproto import sound_pb2

uuid = '87f39d29-7d6d-437d-973b-fba39e49d4ee'

def configure_server():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(('', bluetooth.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    bluetooth.advertise_service(server_sock, 'ANCServer', service_id=uuid,
                                service_classes=[uuid, bluetooth.ADVANCED_AUDIO_CLASS],
                                profiles=[bluetooth.ADVANCED_AUDIO_PROFILE]
                                )

    logging.info(f'Waiting for connection on RFCOMM channel {port}')
    return server_sock

def wait_on_client_connection(server_sock):
    client_sock, client_info = server_sock.accept()
    logging.info(f'Accepted connection from {client_info}')
    return client_sock

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
    soundwave = get_message(socket, sound_pb2.SoundWave)
    wave = np.empty((0,2))
    for i in soundwave.samples:
        sample_arr = np.array([[i.first, i.second]])
        wave = np.concatenate((wave, sample_arr), axis=0)

    return wave

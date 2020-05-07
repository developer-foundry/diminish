import sound_pb2
import sys
import bluetooth
import struct

def socket_read_n(sock, n):
    buf = bytes()
    while n > 0:
        data = sock.recv(n)
        if data == '':
            raise RuntimeError('unexpected connection close')
        buf += data
        n -= len(data)
        print(f'Read {len(data)} bytes and have {n} to go')
    return buf

def get_message(sock, msgtype):
    len_buf = socket_read_n(sock, 4)
    msg_len = struct.unpack('>L', len_buf)[0]
    print(f'Message length: {msg_len}')
    msg_buf = socket_read_n(sock, msg_len)

    msg = msgtype()
    msg.ParseFromString(msg_buf)
    return msg

if __name__ == "__main__":
  uuid = '87f39d29-7d6d-437d-973b-fba39e49d4ee'
  addr = None

  print('Searching for ANC service')
  service_matches = bluetooth.find_service(uuid=uuid, address=addr)

  if len(service_matches) == 0:
      print('Could not find the ANC service.')

  first_match = service_matches[0]
  port = first_match['port']
  name = first_match['name']
  host = first_match['host']

  print('Connecting to \'{}\' on {}'.format(name, host))

  socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
  socket.connect((host, port))
  print('Connected to ANC server')

  soundwave = get_message(socket, sound_pb2.SoundWave)

  print(soundwave.name)
  print(len(soundwave.samples))
  print(soundwave.samples[0])
  print(soundwave.samples[len(soundwave.samples) - 1])


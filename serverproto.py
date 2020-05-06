from soundproto import sound_pb2
import bluetooth
import struct
import sys
import csv

def send_message(sock, message):
    s = message.SerializeToString()
    packed_len = struct.pack('>L', len(s))
    sock.sendall(packed_len + s)

if __name__ == "__main__":
  soundwave = sound_pb2.SoundWave()
  soundwave.name = "Input"

  f = open('data/input.csv')
  csv_f = csv.reader(f, delimiter=' ')

  for row in csv_f:
    sample = soundwave.samples.add()
    sample.first = float(row[0])
    sample.second = float(row[1])

  uuid = '87f39d29-7d6d-437d-973b-fba39e49d4ee'
  
  sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
  sock.bind(('', bluetooth.PORT_ANY))
  sock.listen(1)

  port = sock.getsockname()[1]

  bluetooth.advertise_service(sock, 'ANCServer', service_id=uuid,
                              service_classes=[uuid, bluetooth.ADVANCED_AUDIO_CLASS],
                              profiles=[bluetooth.ADVANCED_AUDIO_PROFILE]
                              )

  client_sock, client_info = sock.accept()
  send_message(client_sock, soundwave)

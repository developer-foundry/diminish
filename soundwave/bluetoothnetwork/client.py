import sys
import bluetooth

uuid = '87f39d29-7d6d-437d-973b-fba39e49d4ee'

def configure_client():
    addr = None

    print('Searching for ANC service')
    service_matches = bluetooth.find_service(uuid=uuid, address=addr)

    if len(service_matches) == 0:
        print('Couldn not find the ANCServer service.')
        sys.exit(0)

    first_match = service_matches[0]
    port = first_match['port']
    name = first_match['name']
    host = first_match['host']

    print('Connecting to \'{}\' on {}'.format(name, host))

    socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    socket.connect((host, port))
    print('Connected to ANC server')
    return socket

def send_data(socket, data):
    print('Sending: ', data)
    return socket.send(data)

def close_connection(socket):
    socket.close()
    print('Disconnected.')
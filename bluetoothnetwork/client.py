import sys
import bluetooth


def setup(serverAddress):
    sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
    port = 0x1001
    print("Trying to connect to {} on PSM 0x{}...".format(serverAddress, port))
    sock.connect((serverAddress, port))
    print("Connected. Type something...")
    while True:
        data = input()
        if not data:
            break
        sock.send(data)
        data = sock.recv(1024)
        print("Data received:", str(data))

    sock.close()
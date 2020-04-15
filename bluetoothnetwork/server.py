import bluetooth

def setup():
    print("Standing up BT server")
    server_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
    port = 0x1001
    server_sock.bind(("", port))
    server_sock.listen(1)

    print("Waiting on connection from client...")
    client_sock, address = server_sock.accept()
    print("Accepted connection from", address)

    data = client_sock.recv(1024)
    print("Data received:", str(data))

    while data:
        client_sock.send("Echo =>", str(data))
        data = client_sock.recv(1024)
        print("Data received:", str(data))

    client_sock.close()
    server_sock.close()
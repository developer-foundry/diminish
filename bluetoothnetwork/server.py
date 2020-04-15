import bluetooth

def setup():
    print("Standing up BT server")
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 0x1001
    server_sock.bind(("", port))
    server_sock.listen(1)
    #uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ef"
    #bluetooth.advertise_service(server_sock, "SampleServerL2CAP",
    #                        service_id=uuid, service_classes = [uuid])

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
import bluetooth

uuid = "87f39d29-7d6d-437d-973b-fba39e49d4ee"

def configure_server():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    bluetooth.advertise_service(server_sock, "ANCServer", service_id=uuid,
                                service_classes=[uuid, bluetooth.ADVANCED_AUDIO_CLASS],
                                profiles=[bluetooth.ADVANCED_AUDIO_PROFILE]
                                )

    print("Waiting for connection on RFCOMM channel", port)
    return server_sock

def wait_on_client_connection(server_sock):
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from", client_info)
    return client_sock

def receive_frame(client_sock):
    try:
        data = client_sock.recv(1024)
        return data
    except OSError:
        pass

def close_connection(client_sock, server_sock):
    client_sock.close()
    server_sock.close()
    print("Disconnected.")
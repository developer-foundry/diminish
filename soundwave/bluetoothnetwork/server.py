import bluetooth
import logging

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

    logging.info('Waiting for connection on RFCOMM channel %d' % port)
    return server_sock

def wait_on_client_connection(server_sock):
    client_sock, client_info = server_sock.accept()
    logging.info('Accepted connection from %s' % client_info)
    return client_sock

def close_connection(client_sock, server_sock):
    client_sock.close()
    server_sock.close()
    logging.info('Bluetooth server from client')
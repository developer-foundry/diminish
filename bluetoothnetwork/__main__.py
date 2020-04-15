import getopt
import wave
import sys
import argparse

from bluetoothnetwork import client
from bluetoothnetwork import server

def clean(inputString):
    if inputString is not None:
        inputString = inputString.strip()
    return inputString

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='POC for bluetooth connection')
        parser.add_argument('-m', dest='mode', action='store', choices=['client', 'server', ' client', ' server'], default='server', type=str,
                            help='Whether you want to run as server or client for POC')
        parser.add_argument('-a', dest='serverAddress', action='store', type=str,
                            help='bluetooth address of the server')
        args = parser.parse_args()
        args.mode = clean(args.mode)
        args.serverAddress = clean(args.serverAddress)

        if args.mode == 'server':
            server.setup()
        elif args.mode == 'client':
            client.setup(args.serverAddress)

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))

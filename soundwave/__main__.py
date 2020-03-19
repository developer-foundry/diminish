import getopt
import wave
import sys
import alsaaudio
import argparse

from soundwave import app

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='POC for ACN testing')
    parser.add_argument('-f', dest='file', action='store', required=True, type=str,
                        help='defines action taken by application. Default = 0')
    parser.add_argument('-d', dest='device', action='store', default='default', type=str,
                        help='defines action taken by application. Default = 0')
    parser.add_argument('-r', dest='mode', action='store', default=0, type=int,
                        help='defines action taken by application. Default = 0')

    args = parser.parse_args()

    device = alsaaudio.PCM(device=args.device)

    if args.mode == 0:
        f = wave.open(args.file, 'rb')
        app.play(device, f)
        f.close()
    elif args.mode == 1:
        app.acn_file(parser, args.device, args.file)
    else:
        f = open(args.file, 'wb')
        app.record(args.device, f)
        f.close()

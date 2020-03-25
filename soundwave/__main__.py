import getopt
import wave
import sys
import alsaaudio
import argparse

from soundwave import app

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='POC for ACN testing')
    parser.add_argument('-f', dest='inputSignal', action='store', required=True, type=str,
                        help='input signal to be used for the ACN algorithm')
    parser.add_argument('-t', dest='targetSignal', action='store', type=str,
                        help='target signal to be used for the ACN algorithm')
    parser.add_argument('-d', dest='device', action='store', default='default', type=str,
                        help='override the default sound device')
    parser.add_argument('-r', dest='mode', action='store', default=0, type=int,
                        help='defines action taken by application. Default = 0')

    args = parser.parse_args()
    args.inputSignal = args.inputSignal.strip()

    if args.targetSignal is not None:
        args.targetSignal = args.targetSignal.strip()

    device = alsaaudio.PCM(device=args.device)

    if args.mode == 0:
        app.play(parser, args.device, args.inputSignal)
    elif args.mode == 1:
        app.acn_file(parser, args.device, args.inputSignal, args.targetSignal)
    else:
        app.record(parser, args.device, args.inputSignal)

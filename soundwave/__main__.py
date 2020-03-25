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
    parser.add_argument('-a', dest='algorithm', action='store', default='lms', required=True, type=str,
                        help='the algorithm to use to process signal. The default is lms.')
    parser.add_argument('-s', dest='size', action='store', default=300000, type=int,
                        help='The size of the file you want to truncate to.')

    args = parser.parse_args()
    args.inputSignal = args.inputSignal.strip()
    args.algorithm = args.algorithm.strip()

    if args.targetSignal is not None:
        args.targetSignal = args.targetSignal.strip()

    device = alsaaudio.PCM(device=args.device)

    app.process(parser, args.device, args.inputSignal,
                args.targetSignal, args.size, args.algorithm)

import getopt
import wave
import sys
import alsaaudio
import argparse

from soundwave import app


def clean(inputString):
    if inputString is not None:
        inputString = inputString.strip()
    return inputString


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='POC for ACN testing')
    parser.add_argument('-i', dest='inputFile', action='store', type=str,
                        help='input file to be used for the ACN algorithm')
    parser.add_argument('-t', dest='targetFile', action='store', type=str, required=True,
                        help='target file to be used for the ACN algorithm')
    parser.add_argument('-d', dest='device', action='store', default='default', type=str,
                        help='override the default sound device')
    parser.add_argument('-a', dest='algorithm', choices=['lms', 'nlms', 'nsslms', ' lms', ' nlms', ' nsslms'], action='store', default='lms', required=True, type=str,
                        help='the algorithm to use to process signal. The default is lms.')
    parser.add_argument('-s', dest='size', action='store', default=300000, type=int,
                        help='The size of the file you want to truncate to.')
    parser.add_argument('-m', dest='mode', action='store', choices=['live', 'prerecorded', ' live', ' prerecorded'], default='live', type=str,
                        help='Whether you want to test a prerecorded file or run algorithm live.')

    args = parser.parse_args()
    args.algorithm = clean(args.algorithm)
    args.mode = clean(args.mode)
    args.inputFile = clean(args.inputFile)
    args.targetFile = clean(args.targetFile)
    device = alsaaudio.PCM(device=args.device)

    if args.mode == 'prerecorded':
        app.process_prerecorded(parser, args.device, args.inputFile,
                                args.targetFile, args.size, args.algorithm)
    elif args.mode == 'live':
        app.process_live(parser, args.device,
                         args.targetFile, args.algorithm)

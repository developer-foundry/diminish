import getopt
import wave
import sys
import alsaaudio

from soundwave import app

if __name__ == '__main__':
    devicestr = 'default'
    mode = 0 # 0 = play, 1 = record

    opts, args = getopt.getopt(sys.argv[1:], 'd:r:')
    for o, a in opts:
        if o == '-d':
            devicestr = a
        if o == '-r':
            mode = a

    if not args:
        print('usage: soundwave [-d <device>] [-r <mode>] <file>', file=sys.stderr)
        sys.exit(2)

    device = alsaaudio.PCM(device=devicestr)

    if mode == 0:
        f = wave.open(args[0], 'rb')
        app.play(device, f)
        f.close()
    else:
        f = open(args[0], 'wb')
        app.record(devicestr, f)
        f.close()

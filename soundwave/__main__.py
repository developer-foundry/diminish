import getopt
import wave
import sys
import alsaaudio

from soundwave import app

if __name__ == '__main__':
    device = 'default'

    opts, args = getopt.getopt(sys.argv[1:], 'd:')
    for o, a in opts:
        if o == '-d':
            device = a

    if not args:
        app.usage()

    f = wave.open(args[0], 'rb')
    device = alsaaudio.PCM(device=device)

    app.play(device, f)

    f.close()

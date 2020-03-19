from __future__ import print_function
import sys
import time
import alsaaudio
import sounddevice as sd
import soundfile as sf


def acn_file(parser, device, f):

    try:
        data, fs = sf.read(f, dtype='float32')
        sd.play(data, fs, device=device)
        status = sd.wait()
    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))
    if status:
        parser.exit('Error during playback: ' + str(status))

def play(device, f):

    print('%d channels, %d sampling rate\n' % (f.getnchannels(),
                                               f.getframerate()))
    # Set attributes
    device.setchannels(f.getnchannels())
    device.setrate(f.getframerate())

    # 8bit is unsigned in wav files
    if f.getsampwidth() == 1:
        device.setformat(alsaaudio.PCM_FORMAT_U8)
    # Otherwise we assume signed data, little endian
    elif f.getsampwidth() == 2:
        device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    elif f.getsampwidth() == 3:
        device.setformat(alsaaudio.PCM_FORMAT_S24_3LE)
    elif f.getsampwidth() == 4:
        device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
    else:
        raise ValueError('Unsupported format')

    periodsize = f.getframerate() // 8

    device.setperiodsize(periodsize)

    data = f.readframes(periodsize)
    while data:
        # Read data from stdin
        device.write(data)
        data = f.readframes(periodsize)


def record(device, f):
    # Open the device in nonblocking capture mode. The last argument could
    # just as well have been zero for blocking mode. Then we could have
    # left out the sleep call in the bottom of the loop
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,
                        alsaaudio.PCM_NONBLOCK, device=device)

    # Set attributes: Mono, 44100 Hz, 16 bit little endian samples
    inp.setchannels(2)
    inp.setrate(44100)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

    # The period size controls the internal number of frames per period.
    # The significance of this parameter is documented in the ALSA api.
    # For our purposes, it is suficcient to know that reads from the device
    # will return this many frames. Each frame being 2 bytes long.
    # This means that the reads below will return either 320 bytes of data
    # or 0 bytes of data. The latter is possible because we are in nonblocking
    # mode.
    inp.setperiodsize(160)

    loops = 1000000
    while loops > 0:
        loops -= 1
        # Read data from device
        l, data = inp.read()

        if l:
            f.write(data)
            time.sleep(.001)

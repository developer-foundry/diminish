import sounddevice as sd
import soundfile as sf


def play_signal(parser, signal, fs, device):
    try:
        sd.play(signal, fs, device=device)
        status = sd.wait()
        if status:
            parser.exit('Error during playback: ' + str(status))

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))


def play_file(parser, device, f):
    try:
        data, fs = sf.read(f, dtype='float32')
        sd.play(data, fs, device=device)
        status = sd.wait()
        if status:
            parser.exit('Error during playback: ' + str(status))

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))

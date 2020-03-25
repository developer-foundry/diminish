import sounddevice as sd
import soundfile as sf


def record(parser, device, f):
    duration = 5  # seconds
    frequency = 44100
    myrecording = sd.rec(int(duration * frequency),
                         samplerate=frequency, channels=2)
    sd.wait()
    sf.write(f, myrecording, frequency)

import sounddevice as sd
import soundfile as sf


def record_to_file(parser, device, f):
    duration = 15  # seconds
    frequency = 44100
    myrecording = sd.rec(int(duration * frequency),
                         samplerate=frequency, channels=2)
    sd.wait()
    sf.write(f, myrecording, frequency)


def record_to_stream(parser, device, channels, samplerate, audio_callback):
    stream = sd.InputStream(
        device=device, channels=channels,
        samplerate=samplerate, callback=audio_callback)
    return stream

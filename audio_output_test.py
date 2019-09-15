#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import pyaudio
import numpy as np

RATE = 44100
CHUNK = 1024


p = pyaudio.PyAudio()

player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

for i in range(int(10 * (RATE/CHUNK))):
    player.write(np.fromstring(stream.read(CHUNK),dtype=np.int16))

stream.stop_stream()
stream.close()
p.terminate()

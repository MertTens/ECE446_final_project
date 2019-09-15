#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import pyaudio
import numpy as np
import time

RATE = 44100
CHUNK = 16384


p = pyaudio.PyAudio()

player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Note: since the write command hangs on write until the audio from it is played, it is probably best to 
# have a low audio 'frame rate' so the sound is not as choppy (at least for now)
# The ideal way to fix this would be to somehow have oscillators that can play even though the code is running
# It looks like pyaudio is able to do non-blocking reads and writes, look into this

for i in range(int(10 * (RATE/CHUNK))):
    player.write(np.fromstring(stream.read(CHUNK, exception_on_overflow=False),dtype=np.int16))

stream.stop_stream()
stream.close()
p.terminate()

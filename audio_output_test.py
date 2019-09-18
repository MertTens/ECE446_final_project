#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import pyaudio
import numpy as np
import time
import math

RATE = 44100
CHUNK = 4096
volume = 1
f = 440.0
duration = 3


def sine_wave(frequency = 440.0, rate = RATE, vol = volume):
    return((np.sin(2 * np.pi * np.arange(rate / frequency) * frequency / rate)).astype(np.float32))


def normalize(array):
    factor = max(np.abs(np.amin(array)), np.amax(array))
    return(array/factor)

thing = sine_wave()


samples = sine_wave().tobytes()


p = pyaudio.PyAudio()

player = p.open(format=pyaudio.paFloat32, channels=1, rate=RATE, output=True)
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Note: since the write command hangs on write until the audio from it is played, it is probably best to 
# have a low audio 'frame rate' so the sound is not as choppy (at least for now)
# The ideal way to fix this would be to somehow have oscillators that can play even though the code is running
# It looks like pyaudio is able to do non-blocking reads and writes, look into this



a_index = 0
a_sine = sine_wave()
a_length = len(a_sine)

c_index = 0
c_sine = sine_wave(523.25)
c_length = len(c_sine)

sines = [sine_wave(440.0), sine_wave(523.25), sine_wave(659.25), sine_wave(783.99)]
indices = [0, 0, 0, 0]
lengths = [len(sines[0]), len(sines[1]), len(sines[2]), len(sines[3])]

while True:
    data = []
    for i in range(CHUNK):
#        a_index = (a_index + 1) % a_length
#        c_index = (c_index + 1) % c_length
#        new_data_value = a_sine[a_index] + c_sine[c_index]

        new_data_value = 0
        for j in range(len(sines)):
            indices[j] = (indices[j] + 1) % lengths[j]
            new_data_value = new_data_value + sines[j][indices[j]]
        data.append(new_data_value)
    
    new_data = np.asarray(normalize(data), dtype=np.float32)
    player.write(new_data.tobytes())
        


stream.stop_stream()
stream.close()
p.terminate()

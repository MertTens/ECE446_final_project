#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import pyaudio
import numpy as np
import time
import math

RATE = 44100
CHUNK = 16384
chans = 1
volume = 1
f = 440.0
duration = 3
frequencies = [440, 525.3]

def sine(current_time, frequency=440):
    length = CHUNK
    factor = float(frequency) * (math.pi * 2) / RATE
    this_chunk = numpy.arange(length) + current_time
    return numpy.sin(this_chunk * factor)

def get_chunk():
    data = sine(time.time())
    return data * 0.1

def callback(in_data, frame_count, time_info, status):
    chunk = get_chunk() * 0.25
    data = chunk.astype(numpy.float32).tostring()
    return (data, pyaudio.paContinue)


def sine_wave(frequency = 440.0, rate = RATE, vol = volume):
    return((np.sin(2 * np.pi * np.arange(rate / frequency) * frequency / rate)).astype(np.float32))


def normalize(array):
    factor = max(np.abs(np.amin(array)), np.amax(array))
    if factor != 0:
        ret = array/factor
    else:
        ret = array
    return(array/factor)

def convert_to_2_channels(left, right):
    stereo = []
    for i in range(len(left)):
        stereo.append(left[i])
        stereo.append(right[i])    

#def callback(in_data, frame_count, time_info, flag):
#    print(frame_count)
#    return(in_data, pyaudio.paContinue)

#sines = [sine_wave(440.0), sine_wave(523.25), sine_wave(659.25), sine_wave(783.99)]
#indices = [0, 0, 0, 0]
#lengths = [len(sines[0]), len(sines[1]), len(sines[2]), len(sines[3])]

sines = []
indices = []
lengths = []
volumes_left = []
volumes_right = []

for i in range(len(frequencies)):
    sines.append(sine_wave(frequencies[i]))
    indices.append(0)
    volumes_left.append(1)
    volumes_right.append(1)
    lengths.append(len(sines[i]))

p = pyaudio.PyAudio()

player = p.open(format=pyaudio.paFloat32, channels=chans, rate=RATE, output=True, frames_per_buffer=CHUNK, stream_callback=callback)
player.start_stream()
#stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Note: since the write command hangs on write until the audio from it is played, it is probably best to 
# have a low audio 'frame rate' so the sound is not as choppy (at least for now)
# The ideal way to fix this would be to somehow have oscillators that can play even though the code is running
# It looks like pyaudio is able to do non-blocking reads and writes, look into this

while True:
    time.sleep(1)
#    data_left = []
#    data_right = []
#    for i in range(CHUNK):
#        a_index = (a_index + 1) % a_length
#        c_index = (c_index + 1) % c_length
#        new_data_value = a_sine[a_index] + c_sine[c_index]

#        new_data_value_left = 0
#        new_data_value_right = 0
#        volumes[1] = (volumes[1] + 0.00001) % 1
#        for j in range(len(sines)):
#            indices[j] = (indices[j] + 1) % lengths[j]
#            new_data_value_left = new_data_value_left + volumes_left[j] * sines[j][indices[j]]
#            new_data_value_right = new_data_value_right + volumes_right[j] * sines[j][indices[j]]
#        data_left.append(new_data_value_left)
#        data_right.append(new_data_value_right)
    
#    new_data_left = normalize(data_left)
#    new_data_right = np.asarray(normalize(data_right), dtype=np.float32)
#    new_data = np.asarray(convert_to_2_channels(new_data_left, new_data_right), dtype=np.float32)
#    player.write(new_data_right.tobytes())
        


player.stop_stream()
player.close()
p.terminate()

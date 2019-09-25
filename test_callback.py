#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import time
import numpy as np
import pyaudio
import math

RATE = 44100
CHUNK = 4096
CHUNKS = 1024
chans = 2
volume = 1
f = 440.0
duration = 3
frequencies = [440, 525.3]
new_data = []
sent_data = np.zeros(1024, dtype=np.float32)
print(sent_data)
def sine(current_time, frequency=440):
    length = CHUNK
    factor = float(frequency) * (math.pi * 2) / RATE
    this_chunk = np.arange(length) + current_time
    return np.sin(this_chunk * factor)

def get_chunk():
    data = sine(time.time())
    return data * 0.1

def callback(in_data, frame_count, time_info, status):
    chunk = get_chunk() * 0.25
    data = chunk.astype(np.float32).tostring()
    thing = sent_data.tobytes()
    data = thing
    print(thing)
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
    return(stereo)

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

stream = p.open(format = pyaudio.paFloat32,
                channels = 2,
                rate = RATE,
                output = True,
                stream_callback = callback)

stream.start_stream()

while True:
    time.sleep(0.1)
    data_left = []
    data_right = []
    for i in range(CHUNKS):
#        a_index = (a_index + 1) % a_length
#        c_index = (c_index + 1) % c_length
#        new_data_value = a_sine[a_index] + c_sine[c_index]

        new_data_value_left = 0
        new_data_value_right = 0
#        volumes[1] = (volumes[1] + 0.00001) % 1
        for j in range(len(sines)):
            indices[j] = (indices[j] + 1) % lengths[j]
            new_data_value_left = new_data_value_left + volumes_left[j] * sines[j][indices[j]]
            new_data_value_right = new_data_value_right + volumes_right[j] * sines[j][indices[j]]
        data_left.append(new_data_value_left)
        data_right.append(new_data_value_right)
    
    new_data_left = np.asarray(normalize(data_left), dtype=np.float32)
    new_data_right = np.asarray(normalize(data_right), dtype=np.float32)
    new_data = np.asarray(convert_to_2_channels(new_data_left, new_data_right), dtype=np.float32)
    sent_data = new_data;
    print(sent_data)
    #player.write(new_data_right.tobytes())

stream.stop_stream()
stream.close()

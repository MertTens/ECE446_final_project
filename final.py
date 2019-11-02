#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import time
import numpy as np
import pyaudio
import math
import cv2
import numpy.core.multiarray

freq_granularity = 15
freq_min = 300
freq_max = 2000
scale_percent = 1
width = 2
height = 1
RATE = 44100
CHUNK = 4096
#CHUNKS = 4096
CHUNKS = 4096
chans = 2
volume = 1
f = 440.0
duration = 3
frequencies = []
new_data = []
sent_data = np.zeros(CHUNKS * chans, dtype=np.float32)
increment = True

freq_top = freq_max - freq_min
cap = cv2.VideoCapture(0)



   # voldex = int((resized[0][0] / 255) * freq_granularity)
   # volumes_left[voldex] = 1
   # voldex = int((resized[0][1] / 255) * freq_granularity)
   # volumes_left[voldex] = 1
   # voldex = int((resized[0][2] / 255) * freq_granularity)
   # volumes_left[voldex] = 1
   # voldex = int((resized[0][3] / 255) * freq_granularity)
   # volumes_left[voldex] = 1
#    voldex = int((resized[0][0] / 255) * freq_granularity)
#    volumes_left[voldex] = 1

def decision_man(width_idx, height_idx, resized):
    voldex = int((resized[height_idx][width_idx] / 255) * freq_granularity)
    # Later willl be otttther loggggic fooooor voooooolume deciiiiiiiiisions
    right_volume = 0
    if (1 - (width_idx / width)) > 0.5:
        right_volume = 1

    left_volume = 0
    if (width / width) > 0.5:
        left_volume = 1
    volumes_left[voldex] = left_volume
    volumes_right[voldex] = right_volume




def sine(current_time, frequency=440):
    length = CHUNK
    factor = float(frequency) * (math.pi * 2) / RATE
    this_chunk = np.arange(length) + current_time
    return np.sin(this_chunk * factor)

def get_chunk():
    data = sine(time.time())
    return data * 0.1

def callback(in_data, frame_count, time_info, status):
    thing = sent_data
    thing = thing.tostring()
    increment = True
    return (thing, pyaudio.paContinue)

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

for i in range(freq_granularity + 1):
    freq = int(freq_min + freq_top * (i / freq_granularity))
    frequencies.append(freq)

print(frequencies)

for i in range(len(frequencies)):
    sines.append(sine_wave(frequencies[i]))
    indices.append(0)
    volumes_left.append(0)
    volumes_right.append(0)
    lengths.append(len(sines[i]))

p = pyaudio.PyAudio()

stream = p.open(format = pyaudio.paFloat32,
                channels = 2,
                rate = RATE,
                output = True,
                stream_callback = callback)

stream.start_stream()

while True:


    for i in range(len(volumes_left)):
        volumes_right[i] = 0
        volumes_left[i] = 0


    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray2 = numpy.flip(gray,1)
    dim = (width, height)

    resized = cv2.resize(gray2, dim, interpolation = cv2.INTER_AREA)

    cv2.imshow('frame',resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#    print(resized[0][0])
    for i in range(height):
        for j in range(width):
            decision_man(j, i, resized)
#    voldex = int((resized[0][0] / 255) * freq_granularity)
#    volumes_left[voldex] = 1
#    voldex = int((resized[0][1] / 255) * freq_granularity)
#    volumes_left[voldex] = 1
#    voldex = int((resized[0][2] / 255) * freq_granularity)
#    volumes_left[voldex] = 1
#    voldex = int((resized[0][3] / 255) * freq_granularity)
#    volumes_left[voldex] = 1
#    time.sleep(0.1)
    data_left = []
    data_right = []
    if True:
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
        increment = False
    else:
        print("false")
    #player.write(new_data_right.tobytes())

stream.stop_stream()
stream.close()

cap.release()
cv2.destroyAllWindows()

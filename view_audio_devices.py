#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import pyaudio
p = pyaudio.PyAudio()
for ii in range(p.get_device_count()):
	print(p.get_device_info_by_index(ii).get('name'))


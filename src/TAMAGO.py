# coding=utf-8
import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import threading
import rospy
from std_msgs.msg import Float64MultiArray

data = []

pa = pyaudio.PyAudio()

format = pyaudio.paInt16
channels = 8
rate = 16000
frames = 1000
duration = 5.0


def listenTAMAGO():
	stream = pa.open(format=format, channels=channels, rate=rate, input=True,
					 frames_per_buffer=frames)

	while True:
		print "start"
		buf = stream.read(frames)

		data.append(np.absolute(np.frombuffer(buf, dtype='int16').reshape(frames, channels) / float(2 ** 15)
								))

		if len(data) > 2:
			data.pop(0)


if __name__ == '__main__':

	rospy.init_node('TAMAGO', anonymous=True)
	move = rospy.Publisher('/move/amount', Float64MultiArray, queue_size=10)  # 音声認識の結果をメインに送る
	direction = {0: 0, 1:45, 2:90, 3:135, 4:180, 5:-135, 6:-90, 7:-45}

	thread = threading.Thread(target=listenTAMAGO, name="thread", args=())
	thread.setDaemon(True)
	thread.start()

	try:
		while True:
			if len(data) > 0:
				resultlist = [np.sum(data[0][:, 0]), np.sum(data[0][:, 1]), np.sum(data[0][:, 2]),
							  np.sum(data[0][:, 3]), np.sum(data[0][:, 4]), np.sum(data[0][:, 5]),
							  np.sum(data[0][:, 6]), np.sum(data[0][:, 7])]
				if np.max(resultlist) > 20:
					print np.argmax(resultlist)

					a = Float64MultiArray()
					a.data.append(0)
					a.data.append(0)
					a.data.append(float(direction[np.argmax(resultlist)]))
					a.data.append(1)
					move.publish(a)

	except KeyboardInterrupt:
		pass

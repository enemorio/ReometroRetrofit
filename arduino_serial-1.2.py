#!/usr/bin/python3
import serial
import time
import sys
import threading
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
#import matplotlib.animation as animation

load_cell = []
time_stream = []
temp_stream = []
stop_prog = False
stopLock = threading.Lock()
factor0 = 1
factor1 = -8587500.00
#serialLock = threading.Lock()

try: 
	arduino = serial.Serial('/dev/ttyACM0', 115200)
	print('Starting connection to arduino. Please wait...')
	time.sleep(1.5)
	arduino.write(b'1')
except (serial.SerialException):
	print('Arduino not connected!')
	sys.exit(1)

def update_data():
	global stop_prog 
	while not stop_prog:
		#serialLock.acquire()
		in0 = str(arduino.readline())
		#serialLock.release()
		in0 = in0.replace('b\'', '')
		in0 = in0.replace('\\r\\n\'', '')
		try:
			in0 = in0.split(' ')
			mag_sw = int(in0[0])
			l_cell = abs(float(in0[1])*factor0 + factor1)
			if mag_sw == 1:
				time_stream.append(time.time())
				load_cell.append(l_cell)
				temp = float(in0[2])
				temp_stream.append(temp)
				print(time.time(), mag_sw, l_cell, temp)
			else:
				pass
		except (ValueError):
			pass
		except (IndexError):
			pass
	
def user_input():
	global stop_prog 
	while not stop_prog:
		user_in = input('Input a command (2-9, q to exit)> ')
		if user_in in '23456789':
			user_in = bytes(user_in, encoding='UTF-8')
			#serialLock.acquire()
			arduino.write(user_in)
			#serialLock.release()
		elif user_in == 'q':
			stopLock.acquire()
			stop_prog = True
			stopLock.release()
			exit0()
		else:
			print('ERROR: Bad command. Choose 2-9')

def main():
	data_thread.start()
	user_thread.start()

def exit0():
	print('Cleaning up and exiting')
	#data_thread.join()
	#user_thread.join()
	arduino.write(b'0')		# Stops arduino serial transmission
	
	mplstyle.use(['ggplot', 'fast'])
	plt.figure(1)			# set a figure number to insert plots into
	plt.subplot(211)		# 211 - numrows, numcols, figure 
	plt.plot(time_stream, load_cell, 'b-', linewidth=1)
	
	plt.subplot(212)
	plt.plot(time_stream, temp_stream, 'r-', linewidth=0.5)
	
	plt.show()
	sys.exit(0)

data_thread = threading.Thread(target=update_data)
user_thread = threading.Thread(target=user_input)

if __name__ == '__main__':
	main()

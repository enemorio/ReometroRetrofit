#!/usr/bin/python3


import serial
import time
import sys
import threading
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
#import matplotlib.animation as animation

time_stream = []
hx711_stream = []
hx711_factor = 1
hx711_offset = -8587900.00
temp0_stream = []
temp1_stream = []
stop_prog = False
stopLock = threading.Lock()

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
		serial_input_string = str(arduino.readline())
		serial_input_string = serial_input_string.lstrip('b\'')
		serial_input_string = serial_input_string.rstrip('\\r\\n\'')
		serial_input_list = serial_input_string.split(' ')
		try:
			# DEBUG:
			#print('RAW:',serial_input_list)
			hx711_value = abs(float(serial_input_list[0]) * 
								hx711_factor + hx711_offset)
			if serial_input_list[3][1] == '1':	#[1] magnetic switch
				time_stream.append(time.time())
				hx711_stream.append(hx711_value)
				if serial_input_list[1] != 'nan':
					temp0_stream.append(float(serial_input_list[1]))
				else:
					temp0_stream.append(None)
				if serial_input_list[2] != 'nan':
					temp1_stream.append(float(serial_input_list[1]))
				else:
					temp1_stream.append(None)
				
				# DEBUG:
				#print(time_stream[-1], hx711_stream[-1], temp0_stream[-1], temp1_stream[-1])
				
			else:
				pass
		except (ValueError):
			pass
		except (IndexError):
			pass
	
def user_input():
	global stop_prog 
	while not stop_prog:
		user_in = input('Input a command (2-9,a,b,c,d or q to exit)> ')
		if user_in in '23456789abcd':
			user_in = bytes(user_in, encoding='UTF-8')
			arduino.write(user_in)
		elif user_in == 'q':
			stop_prog = True
			exit0()
		else:
			print('ERROR: Bad command. Choose 2-9,a,b,c,d or q to exit')

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
	plt.plot(time_stream, hx711_stream, 'b-', linewidth=1)
	
	plt.subplot(212)
	plt.plot(time_stream, temp0_stream, 'r-', linewidth=0.5)
	plt.plot(time_stream, temp1_stream, 'g-', linewidth=0.5)
	
	plt.show()
	sys.exit(0)

data_thread = threading.Thread(target=update_data)
user_thread = threading.Thread(target=user_input)

if __name__ == '__main__':
	main()

#!/usr/bin/python3

import time
import serial
import sys
import threading
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
#import matplotlib.animation as animation

class Arduino_python_interface:

    def __init__(self):
        self.time_stream = []
        self.hx711_stream = []
        self.hx711_factor = 1
        self.hx711_offset = -8586500.00
        self.temp0_stream = []
        self.temp1_stream = []
        self.stop_prog = False
        self.data_thread = threading.Thread(target=self.update_data)
        #self.user_thread = threading.Thread(target=self.user_input)

        
    def connect_arduino(self, dev_handle='/dev/ttyACM0', baudrate=115200):  
        try: 
	        print('Starting connection to Arduino. Please wait 2 seconds...')
	        self.arduino = serial.Serial(dev_handle, baudrate)
	        print(self.arduino)
	        time.sleep(1.5)
	        self.arduino.write(b'1')
        except (serial.SerialException):
	        print('Arduino not connected! Exiting...')
	        sys.exit(1)

    def update_data(self): 
        while not self.stop_prog:
	        serial_input_string = str(self.arduino.readline())
	        serial_input_string = serial_input_string.lstrip('b\'')
	        serial_input_string = serial_input_string.rstrip('\\r\\n\'')
	        serial_input_list = serial_input_string.split(' ')
	        try:
		        # DEBUG:
		        if self.stop_prog == False:
		            print('RAW:',serial_input_list)
		        hx711_value = abs(float(serial_input_list[0]) * 
							        self.hx711_factor + self.hx711_offset)
		        if serial_input_list[3][1] == '1':	#[1] magnetic switch
			        self.time_stream.append(time.time())
			        self.hx711_stream.append(hx711_value)
			        if serial_input_list[1] != 'nan':
				        self.temp0_stream.append(float(serial_input_list[1]))
			        else:
				        self.temp0_stream.append(None)
			        if serial_input_list[2] != 'nan':
				        self.temp1_stream.append(float(serial_input_list[1]))
			        else:
				        self.temp1_stream.append(None)
			
			        # DEBUG:
			        #print(self.time_stream[-1], self.hx711_stream[-1], self.temp0_stream[-1], self.temp1_stream[-1])
		        else:
			        pass
	        except (ValueError):
		        pass
	        except (IndexError):
		        pass
		        
	
    def user_input(self, user_in):
	    if user_in in '23456789abcd':
		    user_in = bytes(user_in, encoding='UTF-8')
		    self.arduino.write(user_in)
	    elif user_in == 'q':
		    self.stop_prog = True
		    self.close(True)
	    else:
		    print('ERROR: Bad command. Choose 2-9,a,b,c,d or q to exit')

    def close(self, exit_program=False):
	    print('Cleaning up and exiting')
	    #data_thread.join()
	    self.arduino.write(b'0')		# Stops self.arduino serial transmission
	
	    mplstyle.use(['ggplot', 'fast'])
	    plt.figure(1)			# set a figure number to insert plots into
	    plt.subplot(211)		# 211 - numrows, numcols, figure 
	    plt.plot(self.time_stream, self.hx711_stream, 'b-', linewidth=1)
	
	    plt.subplot(212)
	    #plt.plot(self.time_stream, self.temp0_stream, 'r-', linewidth=0.5)
	    plt.plot(self.time_stream, self.temp1_stream, 'r-', linewidth=0.5)
	
	    plt.show()
	    print('Close matplotlib graph to exit program')
	    if exit_program == True:
	        sys.exit(0)

    def start(self):
	    self.data_thread.start()


if __name__ == '__main__':
    interface0 = Arduino_python_interface()
    interface0.connect_arduino('/dev/ttyACM0', 115200)
    interface0.start()
    time.sleep(10)
    '''
    interface0.user_input('3')
    time.sleep(1)
    interface0.user_input('2')
    interface0.user_input('5')
    time.sleep(1)
    interface0.user_input('4')
    interface0.user_input('7')
    time.sleep(1)
    interface0.user_input('6')
    interface0.user_input('9')
    time.sleep(1)
    interface0.user_input('8')
    interface0.user_input('b')
    time.sleep(1)
    interface0.user_input('a')
    interface0.user_input('d')
    time.sleep(1)
    interface0.user_input('c')
    time.sleep(1)
    '''
    print(len(interface0.time_stream))    
    interface0.user_input('q')

    

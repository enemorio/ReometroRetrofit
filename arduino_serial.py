import serial

arduino0 = serial.Serial('/dev/ttyACM0', 57600)
sida = input('Write something to start > ')
sida = bytes(sida, encoding='UTF-8')
arduino0.write(sida)


try:
  while True:
    in0 = str(arduino0.readline())
    in0 = in0.replace('b\'', '')
    in0 = in0.replace('\\r\\n\'', '')
    #in0 = float(in0)
    print(in0)
except (KeyboardInterrupt):
  print('Cleaning up and exiting')

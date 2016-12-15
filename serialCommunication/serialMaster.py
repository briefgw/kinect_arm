# Karl Preisner
# First, this establishes a connection with arduino over serial usb
# It then sends a message. 
# Then it waits.
# Then it prints out what the arduino sends back .

import serial, time

port = '/dev/cu.usbmodem1411'
arduino = serial.Serial(port, 9600, timeout = .1)
time.sleep(2) #give the connection two seconds to settle

arduino.write("Hello from Python!")


x = 5
while x > 0:
	# arduino.write("hello world")
	data = arduino.readline()
	# print data
	if data:
		print data
		# print data.rstrip('\n') #strip out the new lines for now
		# (better to do .read() in the long run for this reason
	x = x-1
	time.sleep(1)






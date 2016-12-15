# Karl Preisner
# This only works with Arduino Sketch: SerialPythonSlaveGearbox


# First, this establishes a connection with arduino over serial usb


import serial, time

port = '/dev/cu.usbmodem1411'
arduino = serial.Serial(port, 9600, timeout = .1)

print "Establishing connection with Arduino.."
time.sleep(2) #give the connection two seconds to settle




print "\nmove gearboxServo to leftPosition -Master"
arduino.write("move gearboxServo to leftPosition")
for i in range(1,100): # wait for 10 seconds to hear a response from Arduino
	# arduino.write("hello world")
	data = arduino.readline()
	# print data
	if data:
		print data
		# print data.rstrip('\n') #strip out the new lines for now
		# (better to do .read() in the long run for this reason
	time.sleep(.1)



print "move gearboxServo to rightPosition -Master"
arduino.write("move gearboxServo to rightPosition")
for i in range(1,100): # wait for 10 seconds to hear a response from Arduino
	# arduino.write("hello world")
	data = arduino.readline()
	# print data
	if data:
		print data
		# print data.rstrip('\n') #strip out the new lines for now
		# (better to do .read() in the long run for this reason
	time.sleep(.1)
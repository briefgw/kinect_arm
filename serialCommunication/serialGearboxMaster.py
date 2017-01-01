# Karl Preisner
# This only works with Arduino Sketch: SerialPythonSlaveGearbox


# First, this establishes a connection with arduino over serial usb

import time
import serial
import serial.tools.list_ports

# port = '/dev/cu.usbmodem1411' # Karl's Mac left USB
# port = '/dev/cu.usbmodem1412' # Karl's Mac right USB

print "Establishing connection with Arduino.."
ports = list(serial.tools.list_ports.comports())
for p in ports:
    try:
    	arduino = serial.Serial(p[0], 9600, timeout = .1)
    	print " - Connection with Arduino established."
    	time.sleep(2) #give the connection two seconds to settle
    	break
    except:
    	pass

# arduino = serial.Serial(port, 9600, timeout = .1)

# print "\nmove gearboxServo to leftPosition -Master"
# arduino.write("move gearboxServo to leftPosition")
# time.sleep(1)

# while True:
# 	time.sleep(0.1)
# 	data = arduino.readline()
	
# 	if data == "moving gearbox to leftPosition now. -Arduino":
# 		print data
# 	elif data == "gearbox movement completed! -Arduino":
# 		print data
# 		break


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



# print "move gearboxServo to rightPosition -Master"
# arduino.write("move gearboxServo to rightPosition")
# for i in range(1,100): # wait for 10 seconds to hear a response from Arduino
# 	# arduino.write("hello world")
# 	data = arduino.readline()
# 	# print data
# 	if data:
# 		print data
# 		# print data.rstrip('\n') #strip out the new lines for now
# 		# (better to do .read() in the long run for this reason
# 	time.sleep(.1)


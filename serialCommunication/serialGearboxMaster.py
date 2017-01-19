# Karl Preisner
# This only works with Arduino Sketch: SerialPythonSlaveGearbox


# First, this establishes a connection with arduino over serial usb
# For some reason, the first write/read takes just under 6 seconds. All
# other writes/reads take around 1.2 seconds

import time
import serial
import serial.tools.list_ports

# port = '/dev/cu.usbmodem1411' # Karl's Mac left USB
# port = '/dev/cu.usbmodem1412' # Karl's Mac right USB

isConnected = False

print "Establishing serial connection with Arduino..."
serialPorts = list(serial.tools.list_ports.comports())

for p in serialPorts: # This needs cleaning. Then put it in the server.
	if "usb" in p[0]:
		try:
			# Open serial connection to arduino.
			arduino = serial.Serial(p[0], 115200, timeout = 0.1)
			time.sleep(2) # give the connection two seconds to settle
	
			# Send a message, wait for a response.
			arduino.write("Are you alive?")
			response = ""
			t_i = time.time()
			for i in range(1,1000): # allow 10 seconds 
				time.sleep(0.01)
				response = arduino.readline()
				if response == "I'm alive! -Arduino":
					print response
					t_f = time.time()
					print " - Time elapsed to receive first response = ", t_f - t_i
					print " - Connection with Arduino established on port = '%s'" %p[0]
					isConnected = True 
					break
		except:
			print " - Connection failed."

if isConnected == False:
	print " - Connection failed. (Check USB connection)"
else:
	# These work~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	print "\nServo Gearbox"
	arduino.write("Servo Gearbox:50")
	t_i = time.time()
	while True:
		response = arduino.readline()
		
		if response == "Begin moving motor. -Arduino":
			print response
			t_f = time.time()
			print " - time elapsed = ", t_f-t_i
			t_i = t_f
		elif response == "Finished moving motor. -Arduino":
			print response
			t_f = time.time()
			print " - time elapsed = ", t_f-t_i
			break

	print "\nLinear Actuator - Middle:60"
	arduino.write("Linear Actuator - Middle:60")
	t_i = time.time()
	while True:
		response = arduino.readline()
		
		if response == "Begin moving motor. -Arduino":
			print response
			t_f = time.time()
			print " - time elapsed = ", t_f-t_i
			t_i = t_f
		elif response == "Finished moving motor. -Arduino":
			print response
			t_f = time.time()
			print " - time elapsed = ", t_f-t_i
			break

	print "\nLinear Actuator - Bottom:100"
	arduino.write("Linear Actuator - Bottom:60")
	t_i = time.time()
	while True:
		response = arduino.readline()
		
		if response == "Begin moving motor. -Arduino":
			print response
			t_f = time.time()
			print " - time elapsed = ", t_f-t_i
			t_i = t_f
		elif response == "Finished moving motor. -Arduino":
			print response
			t_f = time.time()
			print " - time elapsed = ", t_f-t_i
			break



print ""




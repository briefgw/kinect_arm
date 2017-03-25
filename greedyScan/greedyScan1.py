#!/usr/bin/env python

# Karl Preisner
# January 19, 2017
# GUI class for moving all four motors


# motor == 1: "Servo Gearbox:"
# motor == 2: "Linear Actuator - Middle:"
# motor == 3: "Linear Actuator - Bottom:"
# motor == 4: "Stepper Motor (clockwise):"
# motor == 5: "Stepper Motor (counterclockwise):"


from motorServerClientSocket import *
import sys
import time
import subprocess

NC = "\033[0;0m"
BLUE = "\033[0;34m"


print BLUE+"\nHello! Welcome to Karl's greedy scan!"+NC
print "Before we begin, complete these steps:"
print "\t1. Plug RPi and Kinect camera into power. Wait 20 seconds."
print "\t2. Plug RPi into this computer via ethernet cable."
print "\t3. Plug Kinect into this computer via USB cable."
print "\t4. Manually move camera arm to \"Start\" position on table."
print "\t5. Switch motor power block on."
print "\t6. ssh into RPi and execute \'./runServer.sh\'"
print BLUE+"Once you have completed these steps, press "+NC+"\"Enter\""+BLUE+" or exit with "+NC+"\"Ctrl+C\""

raw_input()


# 1. Connect to RPi
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ip_address = "192.168.2.200"
port = 8188

clientSocket = motorServerClientSocket()

print BLUE+"Establishing connection with RPi..."+NC
if clientSocket.connect(ip_address, port):
	print "--Connection established with RPi!"
else:
	sys.exit("--Connection with RPi failed.")



# 2. Move camera arm joints to initial position.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print BLUE+"\nMoving camera arm joint motors to their initial positions:"+NC


# clientSocket.moveMotor("Linear Actuator - Bottom:", 35)

# Move Servo Gearbox:95
clientSocket.moveMotorCommand(1, 95)
if clientSocket.moveMotorResponse() == False:
	print "Error: RPi move motor response."
	sys.exit("--Error moving motor.")

# Move Linear Actuator - Bottom:50
clientSocket.moveMotorCommand(3, 50)
if clientSocket.moveMotorResponse() == False:
	print "Error: RPi move motor response."
	sys.exit("--Error moving motor.")


time.sleep(2) # allow 10 seconds for joint motors to reach their initial positions



# 3. Begin taking images.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
scanProcess = subprocess.Popen('/home/workstation5/workplace/source/cameraarm/3DScanner/scan.sh', stdin=subprocess.PIPE)
time.sleep(3) # allow for the program to load. # do not adjust.



# 4. Move camera arm around table.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Move stepper motor
clientSocket.moveMotorCommand(5, 2500)
if clientSocket.moveMotorResponse() == False:
	print "Error: RPi move motor response."



# 5. Stop taking images.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
time.sleep(1) # we need this sleep here. trust me.
scanProcess.communicate("Stop scanning")



# 6. Disconnect RPi
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
time.sleep(1) # we need this sleep here. trust me.
print BLUE+"\nDisconnected from RPi"+NC
clientSocket.disconnect()


print BLUE+"Scan complete!"+NC
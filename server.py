#!/usr/bin/env python

# Karl Preisner
# December 31, 2016
# This is a server for the Raspberry Pi to accept motor movement commands from a client.

# The arduino is a slave of the Raspberry Pi through serial connection.
# NOTE: Opening/closing/plugging/unplugging the serial port on the Arduino will reset the Aruino application.
# This will return the motors their default positions.

import os
import sys
import socket
import time
import serial
import serial.tools.list_ports

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#       Loopback IP on Mac
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
IP_ADDRESS = "127.0.0.1"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     Raspberry Pi static IP
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IP_ADDRESS = "192.168.2.200"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Port
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PORT = 8188


class rpiserver:
	def __init__(self, ipaddr, port, debug = False):
		
		# Bind to 'ipaddr' on 'port'
		self.port = port
		self.debug = debug
		self.serversocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)  
		self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		self.addr = ipaddr

		if self.debug:
			print "- Binding to",self.addr, "on port", self.port
			self.serversocket.bind((self.addr,self.port))

		if self.debug:
			print "- Listening..."
		self.serversocket.listen(10)


	def accept_connection(self):
		if self.debug:
			print "\nWaiting for connection on", self.addr, "port", self.port
		# this will block until a client connects 
		(self.clientsocket, self.client) = self.serversocket.accept()
		
		# a client has connected to the socket
		# self.clientsocket is a new socket object for reading/writing to client
		if self.debug:
			print "- Connection accepted from", self.clientsocket.getpeername()

		# get the file descriptor from the client socket object
		self.fn = self.clientsocket.fileno()
		
		# create a buffered stream (FILE *) using the file descriptor so that readline() will block for complete lines
		self.fd = os.fdopen(self.fn,'r+')
		if self.debug:
			print "- Opened buffered file descriptor"
		
		# Try to open serial connection to Arduino
		self.isArduinoConnected = False
		self.connectArduino()

		# Send message to client that connection is established.
		self.ImAlive_response()

		return True

	def connectArduino(self):
		if self.isArduinoConnected == False: # this line may not be necessary
			print "- Establishing serial connection with Arduino..."
			serialPorts = list(serial.tools.list_ports.comports())
			for p in serialPorts: # Cycle through all available serial ports
				if "usb" in p[0]:
					try:
						# Open serial connection to arduino.
						self.arduino = serial.Serial(p[0], 115200, timeout = 0.1)
					except:
						print "  - Exception: Could not open serial connection on port '%s'" %p[0]
					time.sleep(2) # give the connection two seconds to settle
					# Check if Arduino is alive.
					if self.isArduinoAlive() == True:
						print "  - Arduino connection established on serial port = '%s'" %p[0]
						self.isArduinoConnected = True 
						break
			if self.isArduinoConnected == False:
				print "  - Arduino connection failed. No port found. (Check USB connection)"

	def isArduinoAlive(self):
		# Send a message, wait for a response.
		# Returns True/False 
		# If false, it sets self.isArduinoConnected = False
		try:
			self.arduino.write("Are you alive?")
			response = ""
			for i in range(1,1000): # allow 5 seconds 
				time.sleep(0.01)
				response = self.arduino.readline()
				if response == "I'm alive! -Arduino":
					return True
		except:
			print "- Exception: Arduino not alive."
		self.isArduinoConnected = False
		return False

	def get_command(self):
		# if self.debug:
		# 	print "Reading line from socket"
		return self.fd.readline()

	def ImAlive_response(self):
		# if self.debug:
		# 	print "I'm alive!"
		self.fd.write("I'm alive!")
		self.fd.flush()

	def send_response(self, msg):
		if self.debug:
			print "-- Sending response: (%s)" %msg
		self.fd.write(msg)
		self.fd.flush()

	def moveMotor(self, command):
		cmdTokens = command.split(':', 1)
		motor = cmdTokens[0]
		value = int(cmdTokens[1])

		if motor == "Servo Gearbox" or motor == "Linear Actuator - Middle" or motor == "Linear Actuator - Bottom":
			self.arduinoMoveMotor(command)
		elif motor == "Stepper Motor (clockwise)" or motor == "Stepper Motor (counterclockwise)":
			self.stepperMoveMotor(motor, value)

	def arduinoMoveMotor(self, command):
		if self.isArduinoConnected == False:
			print "- Arduino not connected. Retrying connection..."
			self.connectArduino()

		# Check if arduino is still connected.
		if self.isArduinoAlive() == True:
			# Send command to arduino.
			# Arduino tokenizes command.
			self.send_response("Begin moving motor")
			time.sleep(10)
			# Arduino sends to responses; wait for both.
			self.send_response("Finished moving motor")
		else:
			self.send_response("Arduino not connected")

	def stepperMoveMotor(self, motor, value):
		# TODO
		if "(counterclockwise)" in motor:
			# move stepper motor "value" steps counterclockwise
			pass
		elif "(clockwise)" in motor:
			# move stepper motor "value" steps clockwise
			pass

		# Send command to stepper program.
		self.send_response("Begin moving motor")
		time.sleep(10)
		self.send_response("Finished moving motor")


if __name__ == "__main__":
	if len(sys.argv) > 1:
		IP_ADDRESS = sys.argv[1]
	if len(sys.argv) > 2:
		PORT = int(sys.argv[2])
	print "\nAccepting connection on %s: %d"%(IP_ADDRESS, PORT)

	# call constructor for rpiserver class
	sv = rpiserver(IP_ADDRESS, PORT, True)
	
	# loop accepting new connections
	while True:
		sv.accept_connection()
		# loop until the readline returns empty line (not even a newline char)
		while True:
			cmd = sv.get_command()

			if len(cmd) <= 0: # client must have closed connection
				print "Closing client socket"
				# graceful shutdown of client socket
				try:
					sv.clientsocket.shutdown(socket.SHUT_RDWR)
				except:
					pass
				# break loop and wait for next connection
				break
			
			# Strip trailing newline from command
			cmd = cmd.rstrip() 

			# Interpret commands received from client
			if cmd == "Are you alive?":
				sv.ImAlive_response()
				continue
			
			if cmd == "Connect to Arduino":
				sv.connectArduino()
				continue

			# Command Received
			print "\nCommand received: (%s)" %cmd
			# Move motor
			sv.moveMotor(cmd)

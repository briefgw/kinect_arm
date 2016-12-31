#!/usr/bin/env python

# Karl Preisner
# December 30, 2016
# This is a server for the Raspberry Pi to accept motor movement commands from a client.

import os
import sys
import socket
import time

IP_ADDRESS = "192.168.2.200"
PORT = 8188


class rpiserver:
	def __init__(self, ipaddr, port, debug = False):
		self.port = port
		self.debug = debug
		self.serversocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)  
		self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		self.addr = ipaddr

		if self.debug:
			print >> sys.stderr, "Binding to ",self.addr, "port", self.port
			self.serversocket.bind((self.addr,self.port))

		if self.debug:
			print >> sys.stderr, "Listening"
		self.serversocket.listen(10)


	def accept_connection(self):
		if self.debug:
			print >> sys.stderr, "Waiting for connection", self.addr, "port", self.port
		# this will block until a client connects 
		(self.clientsocket, self.client) = self.serversocket.accept()
		# a client has connected to the socket
		# self.clientsocket is a new socket object for reading/writing to client
		if self.debug:
			print >> sys.stderr, "Connection accepted from",self.clientsocket.getpeername()

		# get the file descriptor from the client socket object
		self.fn = self.clientsocket.fileno()
		# create a buffered stream (FILE *) using the file descriptor
		# so that readline() will block for complete lines
		self.fd = os.fdopen(self.fn,'r+')
		if self.debug:
			print >> sys.stderr,"Opened buffered file descriptor"
		return True

	def get_command(self):
		if self.debug:
			print >> sys.stderr,"Reading line from socket"
		return self.fd.readline()

	def ImAlive_response(self):
		# if self.debug:
		# 	print >> sys.stderr,"I'm alive!"
		self.fd.write("I'm alive!")
		self.fd.flush()

	def send_response(self, msg):
		if self.debug:
			print >> sys.stderr,"--Sending response: (%s)" %msg
		self.fd.write(msg)
		self.fd.flush()

	def servoGearbox(self, value):
		self.send_response("Begin moving motor")
		time.sleep(10)
		self.send_response("Finished moving motor")

	def middleActuator(self, value):
		self.send_response("Begin moving motor")
		time.sleep(10)
		self.send_response("Finished moving motor")

	def bottomActuator(self, value):
		self.send_response("Begin moving motor")
		time.sleep(10)
		self.send_response("Finished moving motor")

	def stepperClockwise(self, value):
		self.send_response("Begin moving motor")
		time.sleep(10)
		self.send_response("Finished moving motor")

	def stepperCounterclockwise(self, value):
		self.send_response("Begin moving motor")
		time.sleep(10)
		self.send_response("Finished moving motor")

if __name__ == "__main__":
	if len(sys.argv) > 1:
		IP_ADDRESS = sys.argv[1]
	if len(sys.argv) > 2:
		PORT = int(sys.argv[2])
	print >> sys.stderr, "Accepting connection on %s: %d"%(IP_ADDRESS, PORT)

	# call constructor for rpiserver class
	sv = rpiserver(IP_ADDRESS, PORT, True)
	# loop accepting new connections
	while True:
		sv.accept_connection()
		# loop until the readline returns empty line (not even a newline char)
		while True:
			cmd = sv.get_command()

			if len(cmd) <= 0: # client must have closed connection
				print >> sys.stderr,"Closing client socket"
				# graceful shutdown of client socket
				sv.clientsocket.shutdown(socket.SHUT_RDWR)
				# break loop and wait for next connection
				break
			
			# Strip trailing newline from command
			cmd = cmd.rstrip() 

			# Interpret commands received from client
			if cmd == "Are you alive?":
				sv.ImAlive_response()
				continue
			
			# if len(cmd == 0):
			# 	sv.send_response("--Received empty command");

			print >> sys.stderr, "--Command received: (%s)" %cmd
				
			cmdTokens = cmd.split(':', 1)
			motor = cmdTokens[0]
			value = int(cmdTokens[1])

			if motor == "Servo Gearbox":
				sv.servoGearbox(value)
				# sv.send_response("--Response sent = (%s)"%cmd)
			elif motor == "Linear Actuator - Middle":
				sv.middleActuator(value)
			elif motor == "Linear Actuator - Bottom":
				sv.bottomActuator(value)
			elif motor == "Stepper Motor (clockwise)":
				sv.stepperClockwise(value)
			elif motor == "Stepper Motor (counterclockwise)":
				sv.stepperCounterclockwise(value)






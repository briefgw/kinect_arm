# Karl Preisner
# February 25, 2017

# Class for opening client socket connection with RPi motor server.
# - Communitate with RPi motorServer.py
# - Check if values for motor are in motors' ranges.

# Note: all commands sent to the socket must have \n character at the end.

import socket


class motorServerClientSocket:

	def __init__(self): #constructor
		# create client socket
		self.clientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)

		self.ServoGearbox_Range = [65,149]   # degrees
		self.MiddleActuator_Range = [20,140] # degrees
		self.BottomActuator_Range = [20,140] # degrees
		self.StepperMotor_Range = [1,2500]   # steps

	def connect(self, ip_address, port):
		try:
			# connect to client
			self.clientSocket.connect((ip_address, port))
			# wait for "I'm alive" response
			response = self.clientSocket.recv(1000) # blocking 
			print "--RPi response: (%s)" %response
			if response == "I'm alive!":
				return True
		except:
			return False

	def disconnect(self):
		print "\nDisconnected"
		try:
			self.clientSocket.shutdown(socket.SHUT_RDWR)
			self.clientSocket = None
			print "--Socket shutdown complete."
			return True
		except:
			print "--Socket shutdown failed."
			return False
		
	def isConnected(self):
		try:
			self.clientSocket.send("Are you alive?\n")
			response = self.clientSocket.recv(1000) # receive up to 1000 characters (bytes)
			return True
		except:
			return False

	def send(self, command):
		self.clientSocket.send(command)

	def receive(self):
		response = ""
		self.clientSocket.setblocking(0) # set to non-blocking
		try:
			response = self.clientSocket.recv(1000)
		except:
			pass #nothing received from socket
		self.clientSocket.setblocking(1) # set to blocking
		return response

	def getMotorRange(self, motor):
		if motor == 1:
			return self.ServoGearbox_Range
		elif motor == 2:
			return self.MiddleActuator_Range
		elif motor == 3:
			return self.BottomActuator_Range
		elif motor == 4:
			return self.StepperMotor_Range
		elif motor == 5:
			return self.StepperMotor_Range

	def valueInMotorRange(self, motor, value):
		if motor == 1:
			if value < self.ServoGearbox_Range[0] or value > self.ServoGearbox_Range[1]:
				return False
		elif motor == 2:
			if value < self.MiddleActuator_Range[0] or value > self.MiddleActuator_Range[1]:
				return False
		elif motor == 3:
			if value < self.BottomActuator_Range[0] or value > self.BottomActuator_Range[1]:
				return False
		elif motor == 4:
			if value < self.StepperMotor_Range[0] or value > self.StepperMotor_Range[1]:
				return False
		elif motor == 5:
			if value < self.StepperMotor_Range[0] or value > self.StepperMotor_Range[1]:
				return False
		return True

	def moveMotor(self, motor, value):
		if self.valueInMotorRange(motor, value) == False:
			print "--Value not in motor range. Aborting moveMotor."
			return
		m = ""
		if motor == 1:
			m = "Servo Gearbox:"
		elif motor == 2:
			m = "Linear Actuator - Middle:"
		elif motor == 3:
			m = "Linear Actuator - Bottom:"
		elif motor == 4:
			m = "Stepper Motor (clockwise):"
		elif motor == 5:
			m = "Stepper Motor (counterclockwise):"

		command = m + str(value) + "\n" # '\n' needed for socket command
		print "--Sending command: (%s)" %command.rstrip()
		self.clientSocket.send(command)

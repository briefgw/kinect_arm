# Karl Preisner
# December 27, 2016
# Opens a socket connection from server running on raspberry pi

import time
import socket
import sys

IP_ADDRESS = "192.168.0.15"
PORT = 8188

# create client socket
clientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)

isConnected = False

try:
	# Try to connect to socket with IP_ADDRESS and PORT
	clientSocket.settimeout(10)
	clientSocket.connect((IP_ADDRESS, PORT))
	clientSocket.settimeout(None)
	isConnected = True
	print "Connection established"
except:
	print "Connection failed"

# Loop
while isConnected:
	# ping
	try:
		clientSocket.send("hello\n")
		response = clientSocket.recv(1000) #receive up to 1000 characters (bytes)
		isConnected = True
	except:
		isConnected = False

	if isConnected == True:
		command = sys.stdin.readline()
		clientSocket.send(command)

		t = time.time()
		response = clientSocket.recv(1000) #receive up to 1000 characters (bytes)
		
		print "time elapsed = ",time.time()-t
		print response



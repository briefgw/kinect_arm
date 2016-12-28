# Karl Preisner
# December 27, 2016
import socket
import sys

IP_ADDRESS = "192.168.0.15"
PORT = 7777

# create client socket
clientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)

isConnected = False

try:
	# Try to connect to socket with IP_ADDRESS and PORT
	clientSocket.connect((IP_ADDRESS, PORT))
	isConnected = True
	print "Connection established"
except:
	print "Connection failed"

# Loop
while isConnected:

	command = sys.stdin.readline()
	clientSocket.send(command)

	response = clientSocket.recv(1000) #receive up to 1000 characters (bytes)
	print response



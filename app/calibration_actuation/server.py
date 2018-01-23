# Senior Design 2018 - Hatata & Magnan
# The George Washington University

# Import Karl API
# TODO

import socket

def Main():
    HOST = '127.0.0.1' # '' #specifies that the socket is reachable by any address the machine happens to have
    PORT = 5000

    # create and INET, ICP socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a public host, a well-known port
    serversocket.bind((HOST, PORT))

    # Initiate and become server socket
    serversocket.listen(2)
    print("Server Listening...")

    # Read/Write Loop
    while True:
        # accepts connections
        (connsocket, address) = serversocket.accept()
        print("Connection established with: ", address)

        # Read data
        while True:
            data = connsocket.recv(1024)
            if not data: break
            if data == 'Disconnect': break
            print("From connected user: ", data.decode()) # Decode from byte to string to desplay for proof of transfer

            # Do what needs to be done
            print("Request: ", data)

			# Parse for motor number and num_steps
            d_list = data.split(',')
            motor = int(d_list[0])
            num_steps = int(d_list[1])
            # Move stepper motor
            print BLUE+"Begin moving camera arm:"+NC
            print "clientSocket.moveMotorCommand(" + motor + ", " + num_steps + ")"

            connsocket.send(b'Echo=>' + data) # Rencode the data into the byte stream and send back to client

        connsocket.close()

    serversocket.close()
    print "About to disconnect"

if __name__ == '__main__':
    Main()

#!/usr/bin/env python
import os
import sys
import socket
IPADDR="192.168.0.15"
PORT=8188

class rpiserver:
    def __init__(self, ipaddr, port, debug=False):
           self.port=port
           self.debug=debug
           self.serversocket=socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  
           self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
           self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
           self.addr=ipaddr

           if self.debug:
               print >>sys.stderr, "Binding to ",self.addr, "port", self.port
           self.serversocket.bind((self.addr,self.port))

           if self.debug:
               print >>sys.stderr, "Listening"
           self.serversocket.listen(10)


    def accept_connection(self):
           if self.debug:
               print >>sys.stderr, "Waiting for connection ",self.addr, "port", self.port
           # this will block until a client connects 
           (self.clientsocket, self.client) = self.serversocket.accept()
           # a client has connected to the socket
           # self.clientsocket is a new socket object for reading/writing to client
           if self.debug:
               print >>sys.stderr, "Connection accepted from ",self.clientsocket.getpeername()

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

    def send_response(self,msg):
           if self.debug:
               print >> sys.stderr,"Sending response"
           self.fd.write(msg)
           self.fd.flush()

if __name__=="__main__":
    if len(sys.argv) > 1:
            IPADDR = sys.argv[1]
    if len(sys.argv) > 2:
            PORT = int(sys.argv[2])
    print >> sys.stderr, "Accepting connection on %s: %d"%(IPADDR, PORT)

    # call constructor for rpiserver class
    sv = rpiserver(IPADDR,PORT,True)
    # loop accepting new connections
    while True:
        sv.accept_connection()
        # loop until the readline returns empty line (not even a newline char)
        while True:
            cmd=sv.get_command()
            if len(cmd)<=0: # client must have closed connection
               print >> sys.stderr,"Closing client socket"
               # graceful shutdown of client socket
               sv.clientsocket.shutdown(socket.SHUT_RDWR)
               # break loop and wait for next connection
               break
            cmd=cmd.rstrip() # strip trailing newline from command
            print >>sys.stderr, "command received=(%s)"%cmd
            if len(cmd)==0: # probably an empty command with a newline
               sv.send_response("Empty command\n");
            else:
               sv.send_response("Okay: processed (%s)\n"%cmd)

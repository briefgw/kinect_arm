#!/usr/bin/env python

# Karl Preisner
# December 23, 2016
# Control motors with GUI

from motorGUI import *

# loopback ip
# default_IP = "127.0.0.1" 

# RPi static IP
default_IP = "192.168.2.200" # string
default_PORT = 8188 # int

# Build and the motorGUI
root = Tk()
motorGUI = motorGUI(root, default_IP, default_PORT) # make an instance of motorGUI

# Run motorGUI
root.mainloop()

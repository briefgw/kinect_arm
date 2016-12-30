#!/usr/bin/env python

# Karl Preisner
# December 23, 2016
# Control motors with GUI


from motorGUI import *

default_IP = "192.168.2.200" #string
default_PORT = 8188 #int

# Build and run the motorGUI
root = Tk()
gui = motorGUI(root, default_IP, default_PORT) # make an instance of motorGUI

# Main Loop
root.mainloop()

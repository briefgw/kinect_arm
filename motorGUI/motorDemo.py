#!/usr/bin/env python

# Karl Preisner
# December 23, 2016
# Control motors with GUI
import os
import signal
import subprocess

from motorGUI import *

# loopback ip
# default_IP = "127.0.0.1" 

# Run pcl_openni_viewer to see what the Kinect is seeing
pcl_openni_viewer = subprocess.Popen("pcl_openni_viewer", stdout=subprocess.PIPE,shell=True,preexec_fn=os.setsid)

# RPi static IP
default_IP = "192.168.2.200" # string
default_PORT = 8188 # int

# Build and the motorGUI
root = Tk()
motorGUI = motorGUI(root, default_IP, default_PORT) # make an instance of motorGUI

# Run motorGUI
root.mainloop()

# Kill pcl_openni_viewer subprocess (if it is still running)
os.killpg(os.getpgid(pcl_openni_viewer.pid), signal.SIGTERM)
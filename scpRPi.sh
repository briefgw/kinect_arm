#!/bin/bash

# Creator: Karl Preisner
# Created: 23 January 2017

clear
echo "Running script to recursively copy the RPi_code directory into raspberry pi 3 using scp -r."

echo

scp -rp /Users/karlpreisner/Workspace/gwu/seniorDesign/CameraArm/RPi_code karlpi3@192.168.2.200:
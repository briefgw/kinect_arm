#!/usr/bin/expect

# Creator: Karl Preisner
# Created: 23 January 2017

spawn -noecho echo "Script scp RPi_code directory into RPi3 using scp -r."
interact
spawn -noecho scp -rp /Users/karlpreisner/Workspace/gwu/cameraArm/RPi_code karlpi3@192.168.2.200:
expect "assword:"
send "trumpet1\r"
interact
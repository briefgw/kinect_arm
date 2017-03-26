#!/bin/bash

# Karl Preisner
# March 25, 2017

# This script runs the Kinect scanning program and places all scanned 
# images in ./scans/folder1

# If no argument, all scanned images will be placed in ./scans/output.
# All contents of this folder will be overwritten.

# If argument, scanned items will be placed in a directory with that title.
# If this folder exists, it will be overwritten.

# The program karlScan will run in a background process. 
# This script waits for stdin == "Stop scanning" 
# Once it receives that input, it kills the child process. 

# example execution:
#    ./scan.sh folder1
#    >Stop scanning


BLUE="\033[0;34m"
GREEN="\033[0;32m"
MAGENTA="\033[0;35m"
NC="\033[0m"


cd /home/workstation5/workplace/source/cameraarm/3DScanner


cd scans

argv="$1" # get first argument
directory="output"

if [ "$argv" == "" ]; then
	echo -e "${MAGENTA}Overwriting default scan file destination: \n${GREEN}'/home/workstation5/workplace/source/cameraarm/3DScanner/scans/${MAGENTA}$directory'${NC} \nNOTE: existing scan files will be overwritten."
	if [ -d "$directory" ]; then
		rm -rf $directory
	fi
	mkdir $directory
	cd $directory

elif [ ! -d "$argv" ]; then
	directory="$argv"
	echo -e "${MAGENTA}Creating new scan file destination: \n${GREEN}'/home/workstation5/workplace/source/cameraarm/3DScanner/scans/${MAGENTA}$directory'${NC}"
	mkdir $directory
	cd $directory

elif [ -d "$argv" ]; then
	directory="$argv"
	echo -e "${MAGENTA}Overwriting scan file destination: \n${GREEN}'/home/workstation5/workplace/source/cameraarm/3DScanner/scans/${MAGENTA}$directory'${NC}"
	if [ -d "$directory" ]; then
		rm -rf $directory
	fi
	mkdir $directory
	cd $directory
fi

# Reset Kinect camera
echo -e "\n${BLUE}Reset Kinect Camera:${NC}"
killall XnSensorServer

# Begin scan
echo -e -n "\n${BLUE}Start camera feed:${NC}"
/home/workstation5/workplace/source/cameraarm/3DScanner/build/karlScan &
scanPID=$!

# wait for command from stdin to stop scanning.
while true; do
	read var
	if [ "$var" == "Stop scanning" ]; then
		kill $scanPID
		break
	fi
done

echo -e "${BLUE}Finished scanning images.${NC}"
echo -e "${MAGENTA}\nScans saved to: \n${GREEN}'/home/workstation5/workplace/source/cameraarm/3DScanner/scans/${MAGENTA}$directory'${NC}"

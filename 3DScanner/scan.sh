#!/bin/bash

# Karl Preisner
# March 22, 2017

# This script runs the Kinect scanning program and places all scanned 
# images in ./scans/myNewFolder 

# If no argument, all scanned images will be placed in ./scans/output.
# All contents of this folder will be overwritten.

# If argument, scanned items will be placed in a directory with that title.
# If that folder exists, y/n prompt will appear to overwrite contents of that folder.

# The program karlScan will run in a background process. 
# The PID of the backgroun process is written to the file '../../scanPID'
# After 8 seconds, this script terminates the karlScan program.

BLUE="\033[0;34m"
GREEN="\033[0;32m"
NC="\033[0m"

echo -e "${BLUE}Running script './scan.sh'${NC}"

cd scans

argv="$1" # get first argument
directory="output"

if [ "$argv" == "" ]; then
	echo -e "Using default scan file destination: ${GREEN}'./scans/$directory'${NC} \nNOTE: existing scan files will be overwritten."
	if [ -d "$directory" ]; then
		rm -rf $directory
	fi
	mkdir $directory
	cd $directory

elif [ ! -d "$argv" ]; then
	directory="$argv"
	echo "Creating new scan file destination: ${GREEN}'./scans/$directory'${NC}"
	mkdir $directory
	cd $directory

elif [ -d "$argv" ]; then
	directory="$argv"
	echo -e "Scan destination ${GREEN}'./scans/$directory'${NC} already exists. \nDo you wish to overwrite? [Y/n]"
	read -p "" -n 1 -r
	echo
	if [[ $REPLY =~ ^[Yy]$ ]]; then
		rm -rf $directory
		mkdir $directory
		cd $directory
	else
		echo -e "${BLUE}Exiting.${NC}"
		exit
	fi
fi


echo -e "${BLUE}Beginning scan now...${NC}"
killall XnSensorServer
../../build/karlScan &
scanPID=$!
echo $scanPID > ../../scanPID  # write PID of karlScan to file

sleep 8
kill $scanPID
# kill `cat ../../scanPID`        # alternative method of killing

echo -e "${BLUE}Scan complete!${NC}"
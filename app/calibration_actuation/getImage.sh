#!/bin/bash

rm ../../src/Kinect_code/mostRecent.txt

ls -Art | tail -n 1 > .../../src/Kinect_code/mostRecent.txt

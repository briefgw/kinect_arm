#/usr/bin/python

#run with: sudo python test_stepper.py

# April 28, 2016
# Karl Preisner, Bob Forcha

# 1. This is the setup for the Nema 23 stepper motor with M542T Driver. 
# 2. After each stepper movement call, the relative location of the stepper motor, in teeth with repsect to the gear, is written to a file. 
# 3. Move by step or by tooth

# TODO: attach a hall sensor to the arm and a fixed location on the table. Call an initialization() method that scans the entire the table. When the hall sensor is triggered, carefully stop the arm and slowly back up until the hall sensors are lined up again. This location will be fixed and will be tooth 0. 

import RPi.GPIO as GPIO
import time
from sys import argv



#initialize() #TODO: write this method 


# global variables
moveCount = -1 # tracker number for movements
location = 0  # current location
acceleration = 2 #magnitude of linear acceleration

# GPIO pin assignments
pulse_pin = 23
dir_pin = 24
ena_pin = 25

def GPIOsetup():
	# GPIO settings
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(pulse_pin, GPIO.OUT)
	GPIO.setup(dir_pin, GPIO.OUT)
	GPIO.setup(ena_pin, GPIO.OUT)

	GPIO.output(ena_pin, 0)
	GPIO.output(pulse_pin, 0)
	GPIO.output(dir_pin, 0)



# Significant numbers for calculations
motorSteps = 400 # number of steps for 1 cycle of the motor
pulleyTeeth = 40 # number of teeth on the pulley
tableTeeth = 300 # number of teeth on the table gear
stepsPerTooth = motorSteps / pulleyTeeth # = 10 steps
tableSteps = tableTeeth * stepsPerTooth  # = 120000 steps
motorCyclesPerArmCycle = 300/40          # = 7.5 motor cycles


# Predefined SPEEDS

#	10 steps/tooth
#	300 teeth/table rotation
#	120000 steps/table rotation
#	
#	speed 1:	1 step = 0.02sec
#				50 steps/sec
#				table = 60s
#	
#	speed 2:	1 step = 0.016sec
#				62.5 steps/sec
#				table = 48s
#	
#	speed 3:	1 step = 0.012sec
#				83.33~ steps/sec
#				table = 36s
#	
#	speed 4:	1 step = 0.008sec ~~~~~MAX SPEED~~~~~
#				125 steps/sec
#				table = 24s
#	
#	speed 5:	1 step = 0.004sec ~~~~~DO NOT USE~~~~~
#				250 steps/sec
#				table = 12s
#	
#	speed 6:	1 step = 0.002sec ~~~~~DO NOT USE~~~~~
#				500 steps/sec
#				table = 6s
#
#
#	Helpful math:
#	Speed #1: step = 0.02s, 1 rev motor/pulley (400 steps/40 teeth) = 8.0s, 1 rev arm (300 teeth) = 60s


# amount of time (seconds) to take one step
speed1 = 0.02
speed2 = 0.016
speed3 = 0.012
speed4 = 0.008
speed5 = 0.004
speed6 = 0.002





#this function is used for all step functions
def pulse_motor(speed):
	#1 step on motor takes "speed" time
	GPIO.output(pulse_pin, 1)
	time.sleep(speed/2)
	GPIO.output(pulse_pin, 0)
	time.sleep(speed/2)

# writes the relative tooth location of the arm with respect to the table gear
def trackLocation(teeth, direction):
	global moveCount
	moveCount += 1
	if direction == "counter_clockwise":
		global location
		location += + teeth
		location %= tableTeeth
	else:
		if direction == "clockwise":
			location -= teeth
			location %= tableTeeth
			if location < 0:
				location += tableTeeth
	file1.write(str(moveCount) + ": Location = " + str(location) + "\n")










# movement by motor STEP
# step_counter_clockwise
def step_counter_clockwise(steps, speed):  
	GPIO.output(dir_pin, 1)
	for i in range(0, steps):
		pulse_motor(speed)
	trackLocation(steps/stepsPerTooth, "counter_clockwise")

# step_clockwise
def step_clockwise(steps, speed): 
	GPIO.output(dir_pin, 0)
	for i in range(0, steps):
		pulse_motor(speed)
	trackLocation(steps/stepsPerTooth, "clockwise")




# movement by number of TEETH
# teeth_counter_clockwise
def teeth_counter_clockwise(teeth, speed):
	GPIO.output(dir_pin, 1)
	for i in range(0, teeth * stepsPerTooth):
		pulse_motor(speed)
	trackLocation(teeth, "counter_clockwise")

# teeth_clockwise
def teeth_clockwise(teeth, speed):
	GPIO.output(dir_pin, 0)
	for i in range(0, teeth * stepsPerTooth):
		pulse_motor(speed)
	trackLocation(teeth, "clockwise")









#distance covered through acceleration
def distAccel(speed):
	s = 1/speed
	distance = s*s / (2*acceleration)
	return distance

print "At acceleration = %d steps/s^2, %d steps are needed to reach speed = %s\n" % (acceleration, distAccel(speed1), speed1)



#this is not working at all as I had hoped for. Scrap it and try again. speed goes down to get faster
def stepClockwise_accel(steps, speed): #DO NOT RUN UNTIL FIX BELOW
	time = 0
	dist = 0
	for i in range(0, int(distAccel(speed))):
		if time == 0:
			step_speed = 0.2
		else:
			step_speed = dist/time - acceleration*time*0.5
		print "l1 i = %d" %i
		print step_speed
		step_clockwise(1, step_speed)
		dist = dist+1
		time = time + step_speed
	print "finished accelerating!"
	#now move the motor at constant speed
	dist = distAccel(speed)
	time = 0.00001
	#step_clockwise(steps-(2*distAccel(speed)), speed)
	for i in range(0, int(distAccel(speed))):
		step_speed = dist/time + (-1)*acceleration*time*0.5
		#step_clockwise(1, step_speed)
		dist = dist-1
		time += step_speed
	print "hi world"















# write to file the locations of the stepper in this test
filename = "relativeStepperLocation.txt"
print("   writing file: " + filename) #This file keeps track of the relative location of the stepper motor in this session.
file1 = open(filename, 'w')
file1.truncate()
file1.write("This file contains relative location for the current session of the stepper motor.\nRange: 0-300\n")
trackLocation(0, "counter_clockwise")













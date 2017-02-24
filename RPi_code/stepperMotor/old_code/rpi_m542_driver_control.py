#/usr/bin/python

#run with: sudo python test_stepper.py

# April 28, 2016
# Karl Preisner, Bob Forcha

# 1. This is the setup for the Nema 23 stepper motor with M542T Driver. 
# 2. After each stepper movement call, the relative location of the stepper motor, in teeth with repsect to the gear, is written to a file. 
# 3. Move by step or by tooth

# TODO: attach a hall sensor to the arm and a fixed location on the table. Call an initialization() method that scans the entire the table. When the hall sensor is triggered, carefully stop the arm and slowly back up until the hall sensors are lined up again. This location will be fixed and will be tooth 0. 

# initialize() # TODO: write this method 
#TODO: global variable moveCount might not be doing what it is supposed to do in trackLocation()

import RPi.GPIO as GPIO
import time
from sys import argv

# global variables
moveCount = -1 		# tracker number for movements
location = 0  		# current location

# adjustable global variables
acceleration = 100 	# magnitude of linear acceleration 			#10 is a good slow-setting
startSpeed = 10		# initial velocity to begin acceleration	#10 is a good slow-setting


# GPIO pin assignments
pulse_pin = 23 # blue wire
dir_pin = 24 # yellow wire
ena_pin = 25 # green wire

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
#==============\================================\===================
#==============\================================\===================
#==============\===ABOVE CODE IS RASPBERRY PI===\===================
#==============\================================\===================
#==============\================================\===================



# Significant numbers for calculations
motorSteps = 400 # number of steps for 1 cycle of the motor
pulleyTeeth = 40 # number of teeth on the pulley
tableTeeth = 300 # number of teeth on the table gear
stepsPerTooth = motorSteps / pulleyTeeth # = 10 steps
tableSteps = tableTeeth * stepsPerTooth  # = 3000 steps
motorCyclesPerArmCycle = 300/40          # = 7.5 motor cycles

#===================================================================
# Predefined SPEEDS
#		 steps/sec		 sec/step	sec/table
speed1 = 50.0			# 0.020s	60s
speed2 = 62.5			# 0.016s	48s
speed3 = 1/0.012 #83.3~	# 0.012s	36s
speed4 = 125.0			# 0.008s	24s
speed5 = 250.0			# 0.004s	12s
speed6 = 500.0			# 0.002s	6s
#
#	10 steps/tooth
#	300 teeth/table rotation
#	120000 steps/table rotation
#	
#		1/t = s
#		1/s = t	
#
#	Helpful math:
#		Speed #1: step = 0.02s, 1 rev motor/pulley (400 steps/40 teeth) = 8.0s, 1 rev arm (300 teeth) = 60s



#=======================================================
#======================METHODS==========================
#=======================================================

#this function is used for all step functions
def pulse_motor(speed):
	# speed = steps/sec
	# 1/speed = sec/step (what we need)
	# 1 step on motor takes "speed" time
	s = 1/speed
	GPIO.output(pulse_pin, 1)
	time.sleep(s/2)
	GPIO.output(pulse_pin, 0)
	time.sleep(s/2)

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
	if steps > 0:
		GPIO.output(dir_pin, 1)
		for i in range(0, int(steps)):
			pulse_motor(speed)
		trackLocation(steps/stepsPerTooth, "counter_clockwise")
	else:
		print "ERROR in method: step_counter_clockwise(): TYPE: invalid argument: negative distance:"

# step_clockwise
def step_clockwise(steps, speed): 
	if steps > 0:		
		GPIO.output(dir_pin, 0)
		for i in range(0, int(steps)):
			pulse_motor(speed)
		trackLocation(steps/stepsPerTooth, "clockwise")
	else:
		print "ERROR in method: step_clockwise(): TYPE: invalid argument: negative distance:"

#=======================================================================
#=======================================================================
#Get rid of these??

# movement by number of TEETH
# teeth_counter_clockwise
def teeth_counter_clockwise(teeth, speed):
	if teeth > 0:
		GPIO.output(dir_pin, 1)
		for i in range(0, teeth * stepsPerTooth):
			pulse_motor(speed)
		trackLocation(teeth, "counter_clockwise")
	else:
		print "ERROR in method: teeth_counter_clockwise(): TYPE: invalid argument: negative distance:"

# teeth_clockwise
def teeth_clockwise(teeth, speed):
	if teeth > 0:
		GPIO.output(dir_pin, 0)
		for i in range(0, teeth * stepsPerTooth):
			pulse_motor(speed)
		trackLocation(teeth, "clockwise")
	else:
		print "ERROR in method: teeth_clockwise(): TYPE: invalid argument: negative distance:"




#=======================================================================
#=======================================================================
#=======================================================================
#=======================================================================
#=======================================================================



# Distance covered through acceleration
def distAccel(speed):
	distance = speed * speed / (2 * acceleration)
	return distance





# Step CLOCKWISE with Acceleration and Deceleration
def stepClockwise_withAccel(steps, speed):
	if(steps < 0):
		print "ERROR: steps argument cannot be negative!"
		return
	if(speed < 0):
		print "ERROR: speed argument cannot be negative!"	
		return

	
	print "Begin move!"
	print "---Acceleration: %d" % acceleration
	print "---Speed:        %d" % speed
	print "---Total steps:  %d" % steps
	print "---Total acceleration step requirement:  %d steps" % distAccel(speed)
	print "---Total deceleration step requirement:  %d steps" % distAccel(speed)
	print "---Ratio (distAccel(speed)/total steps): %f" % (distAccel(speed) / steps)
	

	#=============================
	accelDist = distAccel(speed) # calculated distance to fully accel to speed
	constDist = steps - (accelDist * 2.0) # calculated distance moving at constant speed
	
	if (constDist < 0):
		accelDist = steps/2.0;
	
	decelDist = accelDist

	if(float(steps)%2.0 == 1):
		print "---Odd number of steps:"		
		if constDist < 0:	
			print "   ---No constant speed. distAccel++"			
			constDist = 0 # go straight from accel to decel
			accelDist = accelDist + 1
		else:
			constDist = steps - accelDist - decelDist # steps moved at constant speed
	else:
		constDist = steps - accelDist - decelDist # steps moved at constant speed
	
	
	#=============================
	# Acelerate
	t0 = time.time()
	totalTime = 0.0
	currSpeed = 0.0 # speed of step at stepCount & currTime	
	print "\n1. Begin Acceleration for %d steps..." %accelDist
	for currStep in range(0, int(accelDist)):
		if totalTime == 0:
			currSpeed = startSpeed #start speed to accelerate
		else:
			currSpeed = (currStep / totalTime) + (acceleration * totalTime * 0.5)
		#print "%d: %d" %(currStep,currSpeed)		
		step_clockwise(1, currSpeed)
		totalTime = totalTime + (1.0/currSpeed)
	print "   ---Finished accelerating!"
	

	#=============================
	# Constant speed	
	if constDist > 0:
		print "2. Moving at constant speed for %d steps..." %constDist	
		step_clockwise(constDist, speed)
		print "   ---Finished moving at constant speed!"
	else:
		print "2. Did not achieve full speed at this acceleration rate." 

		
	#=============================
	# Decelerate
	totalTime = 0
	print "3. Begin Decelerating for %d steps..." %decelDist
	for currStep in range(0, int(decelDist)):
		if totalTime == 0:
			currSpeed = currSpeed #start speed to decelerate
		else:
			currSpeed = (currStep / totalTime) - (acceleration * totalTime * 0.5)
		#print "%d: %d" %(currStep,currSpeed)		
		step_clockwise(1, currSpeed)
		totalTime = totalTime + (1.0/currSpeed)
	print "   ---Finished decelerating!"
	
	print "Run Time: %f seconds\n" % (time.time() - t0)
#end method








#=====================================================================================
#=====================================================================================
# Step COUNTERCLOCKWISE with Acceleration and Deceleration
def stepCounterClockwise_withAccel(steps, speed):
	if(steps < 0):
		print "ERROR: steps argument cannot be negative!"
		return
	if(speed < 0):
		print "ERROR: speed argument cannot be negative!"	
		return

	
	print "Begin move!"
	print "---Acceleration: %d" % acceleration
	print "---Speed:        %d" % speed
	print "---Total steps:  %d" % steps
	print "---Total acceleration step requirement:  %d steps" % distAccel(speed)
	print "---Total deceleration step requirement:  %d steps" % distAccel(speed)
	print "---Ratio (distAccel(speed)/total steps): %f" % (distAccel(speed) / steps)
	

#=============================
	accelDist = distAccel(speed) # calculated distance to fully accel to speed
	constDist = steps - (accelDist * 2.0) # calculated distance moving at constant speed
	
	if (constDist < 0):
		accelDist = steps/2.0;
	
	decelDist = accelDist

	if(float(steps)%2.0 == 1):
		print "---Odd number of steps:"		
		if constDist < 0:	
			print "   ---No constant speed. distAccel++"			
			constDist = 0 # go straight from accel to decel
			accelDist = accelDist + 1
		else:
			constDist = steps - accelDist - decelDist # steps moved at constant speed
	else:
		constDist = steps - accelDist - decelDist # steps moved at constant speed
	
	
	#=============================
	# Acelerate
	t0 = time.time()
	totalTime = 0.0
	currSpeed = 0.0 # speed of step at stepCount & currTime	
	print "\n1. Begin Acceleration for %d steps..." %accelDist
	for currStep in range(0, int(accelDist)):
		if totalTime == 0:
			currSpeed = startSpeed #start speed to accelerate
		else:
			currSpeed = (currStep / totalTime) + (acceleration * totalTime * 0.5)
		#print "%d: %d" %(currStep,currSpeed)		
		step_counter_clockwise(1, currSpeed)
		totalTime = totalTime + (1.0/currSpeed)
	print "   ---Finished accelerating!"
	

	#=============================
	# Constant speed	
	if constDist > 0:
		print "2. Moving at constant speed for %d steps..." %constDist	
		step_counter_clockwise(constDist, speed)
		print "   ---Finished moving at constant speed!"
	else:
		print "2. Did not achieve full speed at this acceleration rate." 

		
	#=============================
	# Decelerate
	totalTime = 0
	print "3. Begin Decelerating for %d steps..." %decelDist
	for currStep in range(0, int(decelDist)):
		if totalTime == 0:
			currSpeed = currSpeed #start speed to decelerate
		else:
			currSpeed = (currStep / totalTime) - (acceleration * totalTime * 0.5)
		#print "%d: %d" %(currStep,currSpeed)		
		step_counter_clockwise(1, currSpeed)
		totalTime = totalTime + (1.0/currSpeed)
	print "   ---Finished decelerating!"
	
	print "Run Time: %f seconds\n" % (time.time() - t0)
#end method












# write to file the locations of the stepper in this test
filename = "./relativeStepperLocation.txt"
print("   writing file: " + filename) #This file keeps track of the relative location of the stepper motor in this session.
file1 = open(filename, 'w')
file1.truncate()
file1.write("This file contains relative location for the current session of the stepper motor.\nRange: 0-300\n")
trackLocation(0, "counter_clockwise")













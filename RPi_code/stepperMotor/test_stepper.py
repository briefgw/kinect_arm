#/usr/bin/python

from rpi_m542_driver_control import *
import RPi.GPIO as GPIO
import time


#setup pins 
GPIOsetup()

# Test with no acceleration
#step_clockwise(motorSteps/2, speed4)
#time.sleep(1.0)

#step_clockwise(tableSteps/4, speed4)
#time.sleep(1.0)





#test with acceleration
print "\nCase 1: Even steps. Constant Speed Achieved."
stepClockwise_withAccel(tableSteps/2, speed6)
time.sleep(1.0)

print "\nCase 2: Even steps. Constant Speed NOT Achieved."
stepClockwise_withAccel(tableSteps/4, speed6)
time.sleep(1.0)

print "\nCase 3: Odd steps. Constant Speed Achieved."
stepClockwise_withAccel(tableSteps/2+1, speed6)
time.sleep(1.0)

print "\nCase 4: Odd steps. Constant Speed NOT Achieved."
stepClockwise_withAccel(tableSteps/4-1, speed6)
time.sleep(1.0)


#teeth_clockwise(pulleyTeeth, speed4)
#time.sleep(1.0)



file1.close()
GPIO.cleanup()

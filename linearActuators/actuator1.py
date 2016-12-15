#/usr/bin/python

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(21,GPIO.OUT)

my_pwm = GPIO.PWM(21,1000)

my_pwm.start(25)
time.sleep(2.0)

my_pwm.ChangeDutyCycle(75)
time.sleep(2.0)

my_pwm.stop()

GPIO.cleanup()

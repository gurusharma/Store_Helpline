import RPi.GPIO as GPIO                           
import os
import sys
import time
GPIO.setmode(GPIO.BOARD)
pir = 32
GPIO.setup(pir, GPIO.IN)
print ("Waiting for sensor to settle")
time.sleep(5)
print ("Detecting motion")
while True:
    if GPIO.input(pir):
            print ("Motion Detected!")
            os.system ("xscreensaver-command -deactivate")
            os.system('python Sqube_Solutions.py')
    else:
            os.system ("xscreensaver-command -activate")
            time.sleep(2)
    time.sleep(0.1)

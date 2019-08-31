#!/usr/bin/env python3

from EmulatorGUI import GPIO
#from EmulatorGUI import GPIO
#from GPIOSimulator import GPIO
#import RPi.GPIO as GPIO
import time
import traceback

def Main():

    try:

        GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)

        GPIO.setup(4, GPIO.OUT)
        GPIO.setup(17, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(18, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(21, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(26, GPIO.IN)

        while True:
            if (GPIO.input(23) == False):
                GPIO.output(4,GPIO.HIGH)
                GPIO.output(17,GPIO.HIGH)
                time.sleep(1)
            if (GPIO.input(15) == True):
                GPIO.output(18,GPIO.HIGH)
                GPIO.output(21,GPIO.HIGH)
                time.sleep(1)
            if (GPIO.input(24) == True):
                GPIO.output(18,GPIO.LOW)
                GPIO.output(21,GPIO.LOW)
                time.sleep(1)
            if (GPIO.input(26) == True):
                GPIO.output(4,GPIO.LOW)
                GPIO.output(17,GPIO.LOW)
                time.sleep(1)

    except Exception as ex:
        traceback.print_exc()
    finally:
        GPIO.cleanup() #this ensures a clean exit

Main()

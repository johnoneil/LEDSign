#!/usr/bin/env python

# TODO: handle actual GPIO module on raspi
#import RPi.GPIO as GPIO
from EmulatorGUI import GPIO

import time
import traceback

MOTION_SENSOR_GPIO_PIN = 23

def Main():

    if True:
        # after: https://www.hackster.io/hardikrathod/pir-motion-sensor-with-raspberry-pi-415c04
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(MOTION_SENSOR_GPIO_PIN, GPIO.IN) #PIR
            
            # Optionally drive a buzzer output
            #GPIO.setup(24, GPIO.OUT) #BUzzer

            time.sleep(2) # to stabilize sensor
            while True:
                if GPIO.input(MOTION_SENSOR_GPIO_PIN): # PIR motion sensor goes high
                    
                    # Optional buzzer output
                    #GPIO.output(24, True)
                    #time.sleep(0.5) #Buzzer turns on for 0.5 sec
                    #GPIO.output(24, False)

                    print("Motion Detected...")
                    time.sleep(5) #to avoid multiple detection
                
                time.sleep(0.1) #loop delay, should be less than detection delay
        except Exception as ex:
            traceback.print_exc()
        finally:
            GPIO.cleanup() #this ensures a clean exit
    else:
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

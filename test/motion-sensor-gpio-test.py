#!/usr/bin/env python

import os
if os.uname()[1] == 'raspberrypi':
    import RPi.GPIO as GPIO
else:
    from EmulatorGUI import GPIO

import time
import traceback

import dbus, dbus.service, dbus.exceptions
import sys

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from gi.repository import GObject as gobject

DBUS_INTERFACE_NAME = 'com.MotionDetectService'
DBUS_OBJECT_PATH = '/com/motiondetect/object'

MOTION_SENSOR_GPIO_PIN = 23

init_gpio = True
obj = None

def emit_signal():
    bus = dbus.SessionBus()
    try:
        obj  = bus.get_object(DBUS_INTERFACE_NAME, DBUS_OBJECT_PATH)

        obj.emitMotionDetectSignal(dbus_interface=DBUS_INTERFACE_NAME)
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)
    
    #reply_handler = handle_reply, error_handler = handle_error)
    return False

def catchall_motiondetect_signals_handler(hello_string):
    print ("Received a hello signal and it says " + hello_string)

def checkGPIO():
    global init_gpio
    global obj
    # after: https://www.hackster.io/hardikrathod/pir-motion-sensor-with-raspberry-pi-415c04
    try:
        if init_gpio:
            init_gpio = False
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(MOTION_SENSOR_GPIO_PIN, GPIO.IN) #PIR
        
            # Optionally drive a buzzer output
            #GPIO.setup(24, GPIO.OUT) #BUzzer

            time.sleep(2) # to stabilize sensor
        if GPIO.input(MOTION_SENSOR_GPIO_PIN): # PIR motion sensor goes high

            print("Motion Detected...")
            emit_signal()

            # Optional buzzer output
            #GPIO.output(24, True)
            #time.sleep(0.5) #Buzzer turns on for 0.5 sec
            #GPIO.output(24, False)

            #time.sleep(5) #to avoid multiple detection
        
        #time.sleep(0.1) #loop delay, should be less than detection delay
    except Exception as ex:
        traceback.print_exc()
        return False
    return True

def Main():
    init_gpio = True
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    try:
        obj  = bus.get_object(DBUS_INTERFACE_NAME, DBUS_OBJECT_PATH)

        obj.connect_to_signal("MotionDetectSignal", catchall_motiondetect_signals_handler, dbus_interface=DBUS_INTERFACE_NAME, arg0="Hello")
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)

    #lets make a catchall
    #bus.add_signal_receiver(catchall_signal_handler, interface_keyword='dbus_interface', member_keyword='member')

    bus.add_signal_receiver(catchall_motiondetect_signals_handler, dbus_interface = DBUS_INTERFACE_NAME, signal_name = "MotionDetectSignal")

    #bus.add_signal_receiver(catchall_motiondetectservice_interface_handler, dbus_interface = DBUS_INTERFACE_NAME, message_keyword='dbus_message')

    gobject.idle_add(checkGPIO, priority=gobject.PRIORITY_HIGH)

    # Initialize a main loop
    DBusGMainLoop(set_as_default=True)
    loop = GLib.MainLoop()
    loop.run()

if __name__ == '__main__':
    Main()

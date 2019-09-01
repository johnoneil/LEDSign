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

class MotionDetectObject(dbus.service.Object):
    '''
    Basic service providing interface to subscribe to
    and generate motion detection events.
    '''
    def __init__(self, conn, object_path=DBUS_OBJECT_PATH):
        dbus.service.Object.__init__(self, conn, object_path)

    @dbus.service.signal(DBUS_INTERFACE_NAME)
    def MotionDetectSignal(self, message):
        # The signal is emitted when this method exits
        # You can have code here if you wish
        pass

    @dbus.service.method(DBUS_INTERFACE_NAME)
    def emitMotionDetectSignal(self):
        '''
        This is the method clients call on the interface when they
        want a "motion detected" event to be propagated to all subscribers
        '''
        #you emit signals by calling the signal's skeleton method
        self.MotionDetectSignal('Hello')
        return 'Signal emitted'

    @dbus.service.method(DBUS_INTERFACE_NAME,
                         in_signature='', out_signature='')
    def Exit(self):
        '''
        This is the method clients call on the interface when they
        want the service to shut down.
        '''
        loop.quit()


def emit_signal(object):
   object.emitMotionDetectSignal()

   return False

def catchall_motiondetect_signals_handler(hello_string):
    print ("Received a hello signal and it says " + hello_string)

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTION_SENSOR_GPIO_PIN, GPIO.IN) #PIR
    # Optionally drive a buzzer output
    #GPIO.setup(24, GPIO.OUT) #BUzzer
    time.sleep(2) # to stabilize sensor

MOTION_SENSOR_PIN_HIGH = False

def checkGPIO(object):
    global MOTION_SENSOR_PIN_HIGH
    # after: https://www.hackster.io/hardikrathod/pir-motion-sensor-with-raspberry-pi-415c04
    try:
        if not MOTION_SENSOR_PIN_HIGH and GPIO.input(MOTION_SENSOR_GPIO_PIN): # PIR motion sensor goes high
            MOTION_SENSOR_PIN_HIGH = True
            print("Motion Detected...")
            emit_signal(object)

            # Optional buzzer output
            #GPIO.output(24, True)
            #time.sleep(0.5) #Buzzer turns on for 0.5 sec
            #GPIO.output(24, False)

        elif MOTION_SENSOR_PIN_HIGH and not GPIO.input(MOTION_SENSOR_GPIO_PIN):
            MOTION_SENSOR_PIN_HIGH = False
        
        #time.sleep(0.1) #loop delay, should be less than detection delay
    except Exception as ex:
        traceback.print_exc()
        return False
    return True

def Main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    # we don't have to check for the service as we're instantiating it here
    session_bus = dbus.SessionBus()
    name = dbus.service.BusName(DBUS_INTERFACE_NAME, session_bus)
    object = MotionDetectObject(session_bus)

    # When the dbus loop is idle we check the GPIO pins and propagate events accordingly
    gobject.idle_add(checkGPIO, object, priority=gobject.PRIORITY_LOW)

    init_gpio()

    # Initialize a main loop
    loop = GLib.MainLoop()
    loop.run()

if __name__ == '__main__':
    Main()

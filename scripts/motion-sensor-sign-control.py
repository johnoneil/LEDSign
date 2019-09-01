#!/usr/bin/env python

import dbus, dbus.service, dbus.exceptions
import sys

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from gi.repository import GObject as gobject

import traceback

from config import MOTION_DETECT_INTERFACE_NAME
from config import MOTION_DETECT_OBJECT_PATH
from config import MOTION_DETECT_SIGN_ON_TIME_MILLISECONDS
from config import SIGN_ENABLE_ON_TIMEOUT_MS
#MOTION_DETECT_SIGN_ON_TIME_MILLISECONDS = 5000
#SIGN_ENABLE_ON_TIMEOUT_MS = 20000

from signon import signon
from signoff import signoff

SIGN_OFF_EVENT_ID = 0
SIGN_CAN_TURN_ON = True
SIGN_ENABLE_ON_EVENT_ID = 0

def enable_sign_on():
    global SIGN_CAN_TURN_ON
    SIGN_CAN_TURN_ON = True

def do_sign_on(do_off_timeout=True, do_enable_timeout=True):
    global SIGN_OFF_EVENT_ID
    global SIGN_CAN_TURN_ON
    global SIGN_ENABLE_ON_EVENT_ID
    # once we go on, we can't be turned on again for X seconds (usually a long time)
    # we also set a timeout when we'll turn the sign off
    # the idea is the sign turns on for a little while on motion but then goes off for several hours
    # so we don't have it constantly turning on/off
    if not SIGN_CAN_TURN_ON:
        return
    signon()
    # hold off turning the sign on again for quite a while
    if SIGN_ENABLE_ON_EVENT_ID > 0:
        gobject.source_remove(SIGN_ENABLE_ON_EVENT_ID)
    if do_enable_timeout:
        SIGN_CAN_TURN_ON = False
        SIGN_ENABLE_ON_EVENT_ID = gobject.timeout_add(SIGN_ENABLE_ON_TIMEOUT_MS, enable_sign_on)

    # remove the previous sign off timeout if it's hanging around
    if SIGN_OFF_EVENT_ID > 0:
        gobject.source_remove(SIGN_OFF_EVENT_ID)
    # add a new timeout for sign turning off
    if do_off_timeout:
        SIGN_OFF_EVENT_ID = gobject.timeout_add(MOTION_DETECT_SIGN_ON_TIME_MILLISECONDS, do_sign_off)

def do_sign_off():
    signoff()

def motiondetect_signal_handler():
    '''
    This gets invoked when the motion detect DBUS signal arrives.
    We have no guarantee about how often this will arive, but it maps to
    motion being detected (i.e. physical voltage on sensor going high).
    '''
    print ("Received motion detecton signal from remote object: " + MOTION_DETECT_OBJECT_PATH)
    # turn the sign on and turn it off again in X seconds
    do_sign_on()

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    try:
        object  = bus.get_object(MOTION_DETECT_INTERFACE_NAME, MOTION_DETECT_OBJECT_PATH)
        object.connect_to_signal("MotionDetectSignal", motiondetect_signal_handler, dbus_interface=MOTION_DETECT_INTERFACE_NAME)
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)

    # sign should start in on state but with no "enable" timeout.
    # it will turn itself off however after N seconds
    do_sign_on(True, False)

    # Initialize a main loop
    DBusGMainLoop(set_as_default=True)
    loop = GLib.MainLoop()
    loop.run()
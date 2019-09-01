#!/usr/bin/env python

import dbus, dbus.service, dbus.exceptions
import sys

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from gi.repository import GObject as gobject

import traceback

from config import MOTION_DETECT_INTERFACE_NAME
from config import MOTION_DETECT_OBJECT_PATH

def motiondetect_signal_handler():
    '''
    This gets invoked when the motion detect DBUS signal arrives.
    We have no guarantee about how often this will arive, but it maps to
    motion being detected (i.e. physical voltage on sensor going high).
    '''
    print ("Received motion detecton signal from remote object: " + MOTION_DETECT_OBJECT_PATH)

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    try:
        object  = bus.get_object(MOTION_DETECT_INTERFACE_NAME, MOTION_DETECT_OBJECT_PATH)
        object.connect_to_signal("MotionDetectSignal", motiondetect_signal_handler, dbus_interface=MOTION_DETECT_INTERFACE_NAME)
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)

    # Initialize a main loop
    DBusGMainLoop(set_as_default=True)
    loop = GLib.MainLoop()
    loop.run()
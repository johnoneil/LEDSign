#!/usr/bin/env python

import dbus, dbus.service, dbus.exceptions
import sys

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from gi.repository import GObject as gobject

import traceback

DBUS_INTERFACE_NAME = 'com.MotionDetectService'
DBUS_OBJECT_PATH = '/com/motiondetect/object'

def handle_reply(msg):
    print(msg)

def handle_error(e):
    print(str(e))

def motiondetect_signal_handler(hello_string):
    print ("Received signal (by connecting using remote object) and it says: "
           + hello_string)

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    try:
        object  = bus.get_object(DBUS_INTERFACE_NAME, DBUS_OBJECT_PATH)

        object.connect_to_signal("MotionDetectSignal", motiondetect_signal_handler, dbus_interface=DBUS_INTERFACE_NAME, arg0="Hello")
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)

    # Initialize a main loop
    DBusGMainLoop(set_as_default=True)
    loop = GLib.MainLoop()
    loop.run()
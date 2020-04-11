#!/usr/bin/env python

import dbus, dbus.service, dbus.exceptions
import sys

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

usage = """Usage:
python example-signal-emitter.py &
python example-signal-recipient.py
python example-signal-recipient.py --exit-service
"""

DBUS_INTERFACE_NAME = 'com.MotionDetectService'
DBUS_OBJECT_PATH = '/com/motiondetect/object'

class MotionDetectObject(dbus.service.Object):
    def __init__(self, conn, object_path=DBUS_OBJECT_PATH):
        dbus.service.Object.__init__(self, conn, object_path)

    @dbus.service.signal(DBUS_INTERFACE_NAME)
    def MotionDetectSignal(self, message):
        # The signal is emitted when this method exits
        # You can have code here if you wish
        pass

    @dbus.service.method(DBUS_INTERFACE_NAME)
    def emitMotionDetectSignal(self):
        #you emit signals by calling the signal's skeleton method
        self.MotionDetectSignal('Hello')
        return 'Signal emitted'

    @dbus.service.method(DBUS_INTERFACE_NAME,
                         in_signature='', out_signature='')
    def Exit(self):
        loop.quit()

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    name = dbus.service.BusName(DBUS_INTERFACE_NAME, session_bus)
    object = MotionDetectObject(session_bus)

    # Initialize a main loop
    DBusGMainLoop(set_as_default=True)
    loop = GLib.MainLoop()
    print("Running example signal emitter service.")
    print(usage)
    loop.run()
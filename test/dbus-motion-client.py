#!/usr/bin/env python

import dbus, dbus.service, dbus.exceptions
import sys

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from gi.repository import GObject as gobject

usage = """Usage:
python example-signal-emitter.py &
python example-signal-recipient.py
python example-signal-recipient.py --exit-service
"""

DBUS_INTERFACE_NAME = 'com.example.TestService'

def handle_reply(msg):
    print(msg)

def handle_error(e):
    print(str(e))

def emit_signal():
   #call the emitHelloSignal method 
   object.emitHelloSignal(dbus_interface=DBUS_INTERFACE_NAME)
                          #reply_handler = handle_reply, error_handler = handle_error)
   # exit after waiting a short time for the signal
   gobject.timeout_add(2000, loop.quit)

   if sys.argv[1:] == ['--exit-service']:
      object.Exit(dbus_interface=DBUS_INTERFACE_NAME)

   return False

def hello_signal_handler(hello_string):
    print ("Received signal (by connecting using remote object) and it says: "
           + hello_string)

def catchall_signal_handler(*args, **kwargs):
    print ("Caught signal (in catchall handler) "
           + kwargs['dbus_interface'] + "." + kwargs['member'])
    for arg in args:
        print("        " + str(arg))

def catchall_hello_signals_handler(hello_string):
    print ("Received a hello signal and it says " + hello_string)
    
def catchall_testservice_interface_handler(hello_string, dbus_message):
    print(DBUS_INTERFACE_NAME + " interface says " + hello_string + " when it sent signal " + dbus_message.get_member())


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    try:
        object  = bus.get_object(DBUS_INTERFACE_NAME, "/com/example/TestService/object")

        object.connect_to_signal("HelloSignal", hello_signal_handler, dbus_interface=DBUS_INTERFACE_NAME, arg0="Hello")
    except dbus.DBusException:
        traceback.print_exc()
        print(usage)
        sys.exit(1)

    #lets make a catchall
    bus.add_signal_receiver(catchall_signal_handler, interface_keyword='dbus_interface', member_keyword='member')

    bus.add_signal_receiver(catchall_hello_signals_handler, dbus_interface = DBUS_INTERFACE_NAME, signal_name = "HelloSignal")

    bus.add_signal_receiver(catchall_testservice_interface_handler, dbus_interface = DBUS_INTERFACE_NAME, message_keyword='dbus_message')

    # Tell the remote object to emit the signal after a short delay
    gobject.timeout_add(2000, emit_signal)

    #loop = gobject.MainLoop()
    # Initialize a main loop
    DBusGMainLoop(set_as_default=True)
    loop = GLib.MainLoop()
    loop.run()
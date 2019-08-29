#!/usr/bin/env python
# vim: set ts=2 expandtab:

import serial
from JetFileII import Message


msg = Message.AutoTest()

#port = '/dev/ttyUSB0'
port = '/dev/ttyACM0'
#port = '/dev/ttyVIRTUAL'
baudrate = 19200

ser = serial.Serial(port, baudrate, timeout=None)

x = ser.write(msg)
y = ser.read()
ser.flushInput()
ser.flushOutput()
ser.close()


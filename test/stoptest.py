#!/usr/bin/env python
# vim: set ts=2 expandtab:

import serial
from JetFileII import Message


msg = Message.StopTest()

port = '/dev/ttyUSB0'
baudRate = 19200

ser = serial.Serial(port, baudRate)
x = ser.write(msg)
ser.close()
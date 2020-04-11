#!/usr/bin/env python
# vim: set ts=2 expandtab:

import serial
from JetFileII import Message


msg = Message.StringFile("Hello there. this is a new writefie implementation.",file_label='hello.txt')


port = '/dev/ttyACM0'
baudRate = 19200
ser = serial.Serial(port, baudRate)
x = ser.write(msg)
ser.close()

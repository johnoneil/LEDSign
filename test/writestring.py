#!/usr/bin/python
# vim: set ts=2 expandtab:

import serial
from JetFileIIProtocol import Message


msg = Message.StringFile("Hello there. this is a new writefie implementation.",file_label='hello.txt')


port = '/dev/ttyS0'
baudRate = 19200
ser = serial.Serial(port, baudRate)
x = ser.write(msg)
ser.close()

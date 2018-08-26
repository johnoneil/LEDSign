#!/usr/bin/env python
# vim: set ts=2 expandtab:

import serial
from JetFileII import Message


msg = Message.TurnSignOff(goodbyeMsg=False)

#print msg.encode("hex")

#print 'size of message is ' + str(len(msg))

port = '/dev/ttyUSB0'
#baudRate = 9600 #19200
baudRate = 19200
ser = serial.Serial(port, baudRate)
x = ser.write(msg)
ser.close()

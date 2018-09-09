#!/usr/bin/env python
# vim: set ts=2 expandtab:

import serial
from JetFileII import Message


msg = Message.StartCountdown(day=10,hour=10,minute=10,second=10)
#msg = Message.EmergencyMessage("What's going on?")

#print msg.encode("hex")

#print 'size of message is ' + str(len(msg))

port = '/dev/ttyUSB0'
baudRate = 19200
ser = serial.Serial(port, baudRate)
x = ser.write(msg)
ser.close()

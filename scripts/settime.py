#!/usr/bin/env python
# vim: set ts=2 expandtab:

import serial
from JetFileII import Message

from config import PORT
from config import BAUD_RATE


msg = Message.SetSystemTime()

print msg.encode('hex')

#port = '/dev/ttyUSB0'
#baudRate = 19200
ser = serial.Serial(PORT, BAUD_RATE)
x = ser.write(msg)
ser.close()

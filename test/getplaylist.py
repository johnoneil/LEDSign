#!/usr/bin/env python
# vim: set ts=2 expandtab:

#******************************************************************************
#
# getplaylist.py
# on-three
# Tuesday, August 28th, 2018
#
# Get playlist off my chainzone led sign via (2).Read System Files (0x0102)
#
#******************************************************************************


import serial
import time
from JetFileII import Font
from JetFileII import Animate
from JetFileII import Format
from JetFileII import Date
from JetFileII import Message

displayMsg = Message.DisplayControlWithoutChecksum

import re

#currently static values for my display
groupAddr = 1
unitAddr = 1
port = '/dev/ttyUSB0'
baudRate = 19200
widthPixels = 128
heightPixels = 32

ser = serial.Serial(port, baudRate)

msg = Message.getSystemFile()

h = ":".join("{:02x}".format(ord(c)) for c in msg)
print(h)

time.sleep(1)
# 'U\xa7O\x13V\x00\x00\x00\x00\x00\xab\xcd\x02\x02\x06\x00SEQUENT.SYS\x00V\x00\x00\x00\x00\x00\x00\x00V\x00\x01\x00\x01\x00\x00\x00SQ\x04\x00\x03\x00\x00\x00ET\x0f\x80\xd8\x07\x03\x10\x00\x00\x01\x01\xd8\x07\x03\x10\x00\x00\x01\x01\xb0\x00\x00\x00ABET\x0f\x80\xd8\x07\x03\x10\x00\x00\x01\x01\xd8\x07\x03\x10\x00\x00\x01\x01\xb0\x00\x00\x00ACET\x0f\x80\xd8\x07\x03\x10\x00\x00\x01\x01\xd8\x07\x03\x10\x00\x00\x01\x01\xb0\x00\x00\x00AD'
print("************getting playlist**********")
print(msg)
x = ser.write(msg)
s = ser.read(len(msg))
print("************response**********")
print(s)
h = ":".join("{:02x}".format(ord(c)) for c in s)
print(h)

ser.close()


#!/usr/bin/python
# vim: set ts=2 expandtab:

#******************************************************************************
#
# weather.py
# John O'Neil
# Monday, March 11th, 2013
#
# Fetch weather via pywapi (python weather api) draw data out of JSON
# and send it to my LED sign.
# This is a test in preparation for an integrated LED sign server type daemon
# that could have something like this as just one small dedicated 'process'.
#
# REQUIRES: debian package "python-pywapi" available in Ubuntu 12.04 or
# google code.
#
#******************************************************************************

import pywapi
import serial
import time
import datetime
from time import mktime
from datetime import datetime
from JetFileIIProtocol import Message
displayMsg = Message.DisplayControlWithoutChecksum


msg = Message.EmergencyMessage('Hello there. How are you?')

print msg.encode("hex")

print 'size of message is ' + str(len(msg))

port = '/dev/ttyS0'
baudRate = 19200
ser = serial.Serial(port, baudRate)
x = ser.write(msg)
ser.close()

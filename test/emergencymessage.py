#!/usr/bin/env python
# vim: set ts=2 expandtab:

#******************************************************************************
#
#   emergencymessage.py
#   Hit sign with an async emergency message
#
#******************************************************************************

import serial
import time
from JetFileII import Message

msg = Message.EmergencyMessage('This is an Emergency!')

#port = '/dev/ttyUSB0'
port = '/dev/ttyACM0'
#port = '/dev/ttyVIRTUAL'
baudRate = 19200

ser = serial.Serial(port, baudRate)

ser.write(msg)

ser.close()

#!/usr/bin/env python
# vim: set ts=2 expandtab:

import serial
from serial import rs485
from JetFileII import Message


msg = Message.TurnSignOff(goodbyeMsg=False)

#port = '/dev/ttyUSB0'
port = '/dev/ttyACM0'
#port = '/dev/ttyVIRTUAL'
#baudRate = 9600 #19200
baudRate = 19200

ser = serial.Serial(port, baudRate)
x = ser.write(msg)

resp = ser.read()
ser.flushInput()
ser.flushOutput()

ser.close()



#!/usr/bin/env python
# vim: set ts=2 expandtab:

import serial
from serial import rs485
from JetFileII import Message


msg = Message.TurnSignOff(goodbyeMsg=False)

#print msg.encode("hex")

#print 'size of message is ' + str(len(msg))

port = '/dev/ttyUSB0'
#baudRate = 9600 #19200
baudRate = 19200
ser = serial.Serial(port, baudRate)
#ser.rs485_mode = rs485.RS485Settings(delay_before_rx=5)


print("************msg**********")
print(msg)
h = ":".join("{:02x}".format(ord(c)) for c in msg)
print(h)

x = ser.write(msg)

r = '' #ser.read(len(msg))
#r = ser.read(12)

print("************response**********")
print(r)
h = ":".join("{:02x}".format(ord(c)) for c in r)
print(h)

ser.close()

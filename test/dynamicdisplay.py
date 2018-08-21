#!/usr/bin/env python
# vim: set ts=2 expandtab:

import serial
from JetFileII import Message
from struct import *

led_sign_width = 128
led_sign_height = 32
#data = bytearray(led_sign_width*led_sign_height/8)#one bit per pixel
data = '\xff' * (led_sign_width*led_sign_height/8)
msgs = Message.DynamicDisplay(data)

#print msg.encode("hex")

#print 'size of message is ' + str(len(msg))

port = '/dev/ttyUSB0'
baudRate = 19200
ser = serial.Serial(port, baudRate)

for i,msg in enumerate(msgs):
  #binary_msg = unpack('C',msg)
  print "MSG " + str(i) + ':' + msg.encode("hex")
  x = ser.write(msg)

ser.close()

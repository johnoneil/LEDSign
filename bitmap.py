#!/usr/bin/python
# vim: set ts=2 expandtab:

import serial
from JetFileIIProtocol import Message
import Image
import time


msg = Message.TurnSignOn()

#print msg.encode("hex")

#print 'size of message is ' + str(len(msg))

#get a microsoft formatted bitmap
data = None
with open ("smile.bmp", "r") as myfile:
  data=myfile.read()

print "length of data is " + str(len(data))
print "and data is  " + data.encode('hex')
print data

msgs = Message.Picture(data,file_label='SMILE')

port = '/dev/ttyS0'
baudRate = 19200
ser = serial.Serial(port, baudRate)
for msg in msgs:
  x = ser.write(msg)
  time.sleep(1)
ser.close()

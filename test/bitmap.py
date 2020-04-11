#!/usr/bin/env python
# vim: set ts=2 expandtab:

import serial
from JetFileII import Message
import time
import sys


#input arguments to this script:
#1st argument: microsoft bitmap to upload to LED sign (monochrome, 256 color supported)
#2nd argument: filename created on sign E partition. Filename max 12 characters.
if(len(sys.argv) != 3):
  print 'USAGE: bitmap.py <bmp file to upload to sign> <filename to write on sign E partition>'
  sys.exit(1)

input_filename = sys.argv[1]
uploaded_filename = sys.argv[2]

#get a microsoft formatted bitmap
data = None
try:
  with open (input_filename, "r") as myfile:
    data=myfile.read()
except IOError:
  print 'ERROR. Problem opening file ' + input_filename
  sys.exit(1)

print 'Uploading file ' + input_filename + ' as file ' + uploaded_filename

#print "length of data is " + str(len(data))
#print "and data is  " + data.encode('hex')
#print data

print("length of data is : " + str(len(data)))

large_picture = True

if large_picture:
  msgs = Message.Picture(data,file_label=uploaded_filename)
  msg = None
else:
  msgs = []
  msg = Message.UploadSmallPicture(data,partition='E', msgId=1)

port = '/dev/ttyACM0'
baudRate = 19200

ser = serial.Serial(port, baudRate)

for m in msgs:
  x = ser.write(m)
  time.sleep(1)

if msg:
  x = ser.write(msg)
  time.sleep(1)
  s = ser.read(len(msg))
  print(s)

ser.close()


#!/usr/bin/env python
# vim: set ts=2 expandtab:

#******************************************************************************
#
# playlist.py
# John O'Neil
# Wednesday, March 13th 2013
#
# Exercise the playlist commands in JetFileII protocol
#
#******************************************************************************


import serial
from JetFileII import Message
displayMsg = Message.DisplayControlWithoutChecksum
import time

files = []
#self, data, msgId, filetype='T',disk='E'
files.append(Message.File('{pause=5}{middle}{moveRightIn}{moveLeftOut}{b16x12}{green}{hhmin_12hr}{nl}{amber}{7x6}{dow_abbr}, {month_abbr} {date} {yyyy}', msgId=1))
files.append(Message.File('{pause=1}{green}{5x5}{moveLeftIn}{moveRightOut}PLAYLIST TWO', msgId=2))
files.append(Message.File('{pause=1}{red}{5x5}{moverightin}{moveRightOut}PLAYLIST THREE', msgId=3))


port = '/dev/ttyUSB0'
baudRate = 19200
ser = serial.Serial(port, baudRate)

playlist = Message.Playlist(files)

for f in files:
  #print msg.data.encode("hex")
  x = ser.write(f.data)
  time.sleep(1)

x = ser.write(playlist)

s = ser.read(len(playlist))
print("************response**********")
print(s)
h = ":".join("{:02x}".format(ord(c)) for c in s)
print(h)

ser.close()


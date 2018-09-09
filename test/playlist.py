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

use_version_2 = True
write_text_files = False

files = []

if True: #write_text_files:
  files.append(Message.TextFile('{pause=5}{middle}{moveRightIn}{moveLeftOut}{b16x12}{green}{hhmin_12hr}{nl}{amber}{7x6}{dow_abbr}, {month_abbr} {date} {yyyy}', msgId=1))
  files.append(Message.TextFile('{pause=1}{green}{5x5}{moveLeftIn}{moveRightOut}xxxPLAYLIST TWO', msgId=2))
  files.append(Message.TextFile('{pause=1}{red}{5x5}{moverightin}{moveRightOut}*\x06\x14_A', msgId=3))
  files.append(Message.TextFile('{pause=1}{amber}{5x5}{moverightin}{moveRightOut}**\x18\x02@A', msgId=4))
  #files.append(Message.SmallPictureFile(None, msgId=1, disk='E', upload=False))
  #files.append(Message.SmallPictureFile(None, msgId=2, disk='D', upload=False))

#file1 = Message.WriteTextFilewithChecksum("hello", "hello.txt")

playlist = None

if use_version_2:
  playlist = Message.WriteSystemFile(Message.PlaylistFileFormat(files))
else:
  playlist = Message.Playlist(files)
  
  #18H + [Length] + 0x0B + [Drive] + [File label]

port = '/dev/ttyUSB0'
baudRate = 19200
ser = serial.Serial(port, baudRate)

if write_text_files:
  for f in files:
    #print msg.data.encode("hex")
    if f.upload:
      x = ser.write(f.data)
      time.sleep(1)

print("*************playlist*************")
print(playlist)
p = ":".join("{:02x}".format(ord(c)) for c in playlist)
print(p)
x = ser.write(playlist)

s = ser.read(len(playlist))
print("************response**********")
print(s)
h = ":".join("{:02x}".format(ord(c)) for c in s)
print(h)

ser.close()


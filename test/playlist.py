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
from JetFileII import TextFile
from JetFileII import SEQUENTSYS
displayMsg = Message.DisplayControlWithoutChecksum
import time

write_text_files = True
write_playlist = True

files = []

if write_text_files:
  #files.append(Message.WriteTextFilewithChecksum( TextFile('MYTESTINGXX1'), "AB.nmg", drive='D'))
  #files.append(Message.WriteTextFilewithChecksum( TextFile('MY OTHER TESTING XX2'), "lngname.nmg", drive='D'))
  files.append(TextFile('{pause=5}{middle}{moveRightIn}{moveLeftOut}{b16x12}{green}{hhmin_12hr}{nl}{amber}{7x6}{dow_abbr}, {month_abbr} {date} {yyyy}', "AB.nmg", drive='D'))
  files.append(TextFile('{pause=1}{green}{5x5}{moveLeftIn}{moveRightOut}xxxPLAYLIST TWO', 'AC.nmg', drive='D'))
  #files.append(Message.TextFile('{pause=1}{red}{5x5}{moverightin}{moveRightOut}*\x06\x14_A', msgId=3))
  #files.append(Message.TextFile('{pause=1}{amber}{5x5}{moverightin}{moveRightOut}**\x18\x02@A', msgId=4))
  #files.append(Message.SmallPictureFile(None, msgId=1, disk='E', upload=False))
  #files.append(Message.SmallPictureFile(None, msgId=2, disk='D', upload=False))


#port = '/dev/ttyUSB0'
#port = '/dev/ttyACM0'
port = '/dev/ttyVIRTUAL'
baudRate = 19200
ser = serial.Serial(port, baudRate)

if write_text_files:
  for f in files:
    print("Sending text file...")
    ser.write(Message.WriteTextFilewithChecksum(f))
    time.sleep(1)

if write_playlist:
  # the actual playlist is a SEQUENT.SYS
  ss = SEQUENTSYS(files)
  # just write the playlist as a system file
  playlist = Message.WriteSystemFile(ss)
  print("*************writing playlist*************")
  ser.write(playlist)

ser.close()

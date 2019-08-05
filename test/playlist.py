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
  files.append(TextFile('{pause=5}{middle}{moveRightIn}{moveLeftOut}{b16x12}{green}{hhmin_12hr}{nl}{amber}{7x6}{dow_abbr}, {month_abbr} {date} {yyyy}', "AB.nmg", drive='D'))
  files.append(TextFile('{pause=1}{green}{5x5}{moveLeftIn}{moveRightOut}Playlist Entry 2', 'AC.nmg', drive='D'))
  files.append(TextFile('{pause=1}{red}{5x5}{moverightin}{moveRightOut}Playlist Entry 3', 'AD.nmg', drive='D'))
  files.append(TextFile('{pause=1}{amber}{5x5}{moverightin}{moveRightOut}Playlist Entry 4', 'AE.nmg', drive='D'))
  #files.append(Message.SmallPictureFile(None, msgId=1, disk='E', upload=False))
  #files.append(Message.SmallPictureFile(None, msgId=2, disk='D', upload=False))


#port = '/dev/ttyUSB0'
#port = '/dev/ttyACM0'
port = '/dev/ttyVIRTUAL'
baudRate = 19200
ser = serial.Serial(port, baudRate)

if write_text_files:
  for f in files:
    print("Writing text file..." + f.label + " to drive: " + f.drive)
    ser.write(Message.WriteTextFilewithChecksum(f))
    time.sleep(1)

if write_playlist:
  # the actual playlist is a SEQUENT.SYS
  ss = SEQUENTSYS(files)
  # just write the playlist as a system file
  playlist = Message.WriteSystemFile(ss)
  print("Writing playlist...")
  ser.write(playlist)

print("Script complete.")

ser.close()

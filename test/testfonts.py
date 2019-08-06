#!/usr/bin/env python
# vim: set ts=2 expandtab:

#******************************************************************************
#
# testFonts.py
# John O'Neil
#
#******************************************************************************


import serial
from JetFileII import Message
from JetFileII import TextFile
from JetFileII import PictureFile
from JetFileII import SEQUENTSYS
displayMsg = Message.DisplayControlWithoutChecksum
import time

test = '{pause=3}{middle}{moveRightIn}{moveRightOut}{amber}FONT TEST{newframe}'
test += '{5x5}5x5{newframe}'
test += '{7x6}7x6{newframe}'
test += '{14x8}14x8{newframe}'
test += '{15x9}15x9{newframe}'
test += '{16x9}16x9{newframe}'
test += '{24x16}24x16{newframe}'
test += '{32x18}32x18{newframe}'
test += '{11x9}11x9{newframe}'
test += '{22x18}22x18{newframe}'
test += '{30x18}30x18{newframe}'
test += '{b14x10}b14x10{newframe}'
test += '{b15x10}b15x10{newframe}'
test += '{b16x12}b16x12{newframe}'

files = []
if True:
  files.append(TextFile(test, "FT.nmg", drive='D'))


#port = '/dev/ttyUSB0'
#port = '/dev/ttyACM0'
port = '/dev/ttyVIRTUAL'
baudRate = 19200
ser = serial.Serial(port, baudRate)

if True:
  for f in files:
    print("Writing file..." + f.label + " to drive: " + f.drive)
    if f.type == 'T':
      ser.write(Message.WriteTextFilewithChecksum(f))
    elif f.type == 'P':
      for packetNumber in range(0,f.numPackets):
        print("Writing image " + f.label + " do drive: " + f.drive + " packet number: " + str(packetNumber))
        ser.write(Message.WritePictureFileWithChecksum(f, packetNumber=packetNumber))
        time.sleep(1)
    time.sleep(1)

if True:
  # the actual playlist is a SEQUENT.SYS
  ss = SEQUENTSYS(files)
  # just write the playlist as a system file
  playlist = Message.WriteSystemFile(ss)
  print("Writing playlist...")
  ser.write(playlist)

print("Script complete.")

ser.close()

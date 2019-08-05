#!/usr/bin/env python
# vim: set ts=2 expandtab:

#******************************************************************************
#
# uploadImage.py
# John O'Neil
# Monday Aug 5th 2019
#
#******************************************************************************


import serial
from JetFileII import Message
from JetFileII import TextFile
from JetFileII import PictureFile
from JetFileII import SEQUENTSYS
displayMsg = Message.DisplayControlWithoutChecksum
import time

#pic = PictureFile('../images/awesome.bmp', 'xd.bmp', 'D')
#pic = PictureFile('../images/g.bmp', 'newg1.bmp', 'D')
pic = PictureFile('../images/mario.bmp', 'mario.bmp', 'D')

#port = '/dev/ttyUSB0'
#port = '/dev/ttyACM0'
port = '/dev/ttyVIRTUAL'
baudRate = 19200

ser = serial.Serial(port, baudRate)

for packetNumber in range(0, pic.numPackets):
  print("Writing image packet " + str(packetNumber))
  ser.write(Message.WritePictureFileWithChecksum(pic, packetNumber=packetNumber))
  time.sleep(1)

print("Script complete.")

ser.close()

#!/usr/bin/env python
# vim: set ts=2 expandtab:

#******************************************************************************
#
# ledsign.py
# John O'Neil
# Saturday, March 9th 2012
#
# Send simple commands to my Chainzone LED sign via JetFileII protocol
#
#******************************************************************************


import serial
import time
from JetFileII import Font
from JetFileII import Animate
from JetFileII import Format
from JetFileII import Date
from JetFileII import Message
displayMsg = Message.DisplayControlWithoutChecksum

import re

#currently static values for my display
groupAddr = 1
unitAddr = 1
port = '/dev/ttyUSB0'
baudRate = 19200
widthPixels = 128
heightPixels = 32

msgs = []

#text = '{ Format.AutoTypeset.Off}{Font.n16x9 }***********ABCDEFG12345*************'
#text = '{red}{5x5}{moverightin}{moveleftout}Testing{nl}{green}{moveRightIn}{noneOut}One{nl}{amber}{moveLeftIn}{moveRightOut}Two{nl}{red}{moveRightIn}{moveLeftOut}Three{nl}{green}Four'
#print text

msgs.append(displayMsg.Create(1,text='{red}{5x5}{moveRightIn}{moveLeftOut}ONE'))
msgs.append(displayMsg.Create(2,text='{green}{5x5}{moveLeftIn}{moveRightOut}TWO'))
msgs.append(displayMsg.Create(3,text='{amber}{5x5}{moverightin}{moveRightOut}THREE'))
#print msg

ser = serial.Serial(port, baudRate)
for msg in msgs:
  print("******* sending msg *********")
  x = ser.write(msg)
  print("************response**********")
  s = ser.read(len(msg))
  print(s);

  time.sleep(1)

ser.close()


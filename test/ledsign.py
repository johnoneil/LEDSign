#!/usr/bin/python
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
from JetFileIIProtocol import Font
from JetFileIIProtocol import Animate
from JetFileIIProtocol import Format
from JetFileIIProtocol import Date
from JetFileIIProtocol import Message
displayMsg = Message.DisplayControlWithoutChecksum

import re

#currently static values for my display
groupAddr = 1
unitAddr = 1
port = '/dev/ttyS0'
baudRate = 19200
widthPixels = 128
heightPixels = 32

#text = '{ Format.AutoTypeset.Off}{Font.n16x9 }***********ABCDEFG12345*************'
text = '{red}{5x5}{moverightin}{moveleftout}Testing{nl}{green}{moveRightIn}{noneOut}One{nl}{amber}{moveLeftIn}{moveRightOut}Two{nl}{red}{moveRightIn}{moveLeftOut}Three{nl}{green}Four'
print text
msg = displayMsg.Create(1,text=text);
print msg

ser = serial.Serial(port, baudRate)
x = ser.write(msg)
ser.close()


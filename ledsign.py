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


#currently static values
groupAddr = 1
unitAddr = 1
port = '/dev/ttyS0'
baudRate = 19200
widthPixels = 128
heightPixels = 32
filename = str('%c%c' % (65 + int(unitAddr / 26), 65 + (unitAddr % 26)))

HEADER = '\x00\x00\x00\x00\x00\x01Z00'
PROTOCOL = '\x06'
CODA = '\x04'
NL = '\x0d'
SLIDE_IN = '\x0aI1'
SLIDE_OUT = '\x0aO1'
MOVE_LEFT_IN = '\x0a'+'I'+'\x31'
MOVE_LEFT_OUT = '\x0a'+'O'+'\x31'
MOVE_RIGHT_IN = '\x0a'+'I'+'\x32'
MOVE_RIGHT_OUT = '\x0a'+'O'+'\x32'
FONT_14X10_BOLD = '\x1aN'
FONT_5X5 = '\x1a0'
FONT_7X6 = '\x1a1'
COLOR_RED = '\x1c\x31'
COLOR_GREEN = '\x1c\x32'
COLOR_AMBER = '\x1c\x33'
COLOR_MIXED_WAVE = '\x1c\x36'
SPEED_SLOWEST = '\x0f6'
SPEED_SLOW = '\x0f5'
SPEED_FAST = '\x0f1' 
SPEED_FASTEST = '\x0f0' 
data = HEADER + '\x02A\x0fET' + filename + PROTOCOL + Format.AutoTypeset.Off + SPEED_FASTEST + Animate.MoveRight.In + Animate.WipeRight.Out +  Font.n7x6 + Font.Color.Red +'1234abcd'+ Format.NewLine + Animate.MoveLeft.In + Animate.MoveLeft.Out + SPEED_SLOW + Font.n14x8 + Font.Color.Green+ Animate.Pause.Seconds(10) + Date.DayOfWeek.Abbreviation + " " + Date.Month.Abbreviation + " " + Date.Day + ", " + Date.YYYY + " " + Format.NewLine + Format.Align.Vertical.Bottom + Format.Align.Horizontal.Left + Animate.Jump.In + Animate.Jump.Out + SPEED_FASTEST + Font.Color.Amber + Font.n5x5 + 'IJKL0123' + CODA
print str(data)

ser = serial.Serial(port, baudRate)
x = ser.write(data)
ser.close()


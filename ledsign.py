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


#currently static values
groupAddr = 1
unitAddr = 1
port = '/dev/ttyS0'
baudRate = 19200
widthPixels = 128
heightPixels = 32
filename = str('%c%c' % (65 + int(unitAddr / 26), 65 + (unitAddr % 26)))

#Simple character based JetFileII protocol
#see section 3.1 'Communication format without CheckSum'
#data = '\x00\x00\x00\x00\x00\x01Z00\x02A\x0f%(drive)cT%(file)s\x06'
#                '\x0aI%(move_in)c'    '\x0aO%(move_out)c' '\x0e20004'
#                '\x1b0%(typeset)c'    '\x081'             '\x1f%(vert_align)c'
#                '\x1e%(horiz_align)c' '\x0f%(speed)c'     '\x1c%(color)c'
#                '\x1d%(background)c'  '\x1a1'     '\x07%(flash)c'
#                '%(text)s'            '\x04'
#data = '\x00\x00\x00\x00\x00\x01Z00\x02A\x0fET%(filename)s\x06Testing my\x0dsoftware now!\x04'% {'filename' : '%c%c' % (65 + int(unitAddr / 26), 65 + (unitAddr % 26))}
#<0x0a>I1ABCD2345<0x0D>EFGH6789<0x0D>IJKL0123
#data = '\x00\x00\x00\x00\x00\x01Z00\x02A\x0fET%(filename)s\x06\x0aI1\x0aO1ABCD2345\x0dEFGH6789\x0dIJKL0123\x04'% {'filename' : '%c%c' % (65 + int(unitAddr / 26), 65 + (unitAddr % 26))}
#data = '\x00\x00\x00\x00\x00\x01Z00\x02A\x0fET%(filename)s\x06\x0aI1\x0aO1BananaTreeGator\x04'% {'filename' : '%c%c' % (65 + int(unitAddr / 26), 65 + (unitAddr % 26))}
#data = '\x00\x00\x00\x00\x00\x01Z00\x02A\x0fET%(filename)s\x06\x0aI1\x0aO1\x1aN\x1c\x36ABCD2345\x0dEFGH6789\x0dIJKL0123\x04'% {'filename' : '%c%c' % (65 + int(unitAddr / 26), 65 + (unitAddr % 26))}
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
data = HEADER + '\x02A\x0fET' + filename + PROTOCOL + SPEED_FASTEST + MOVE_LEFT_IN + MOVE_LEFT_OUT +  Font.n7x6 + COLOR_RED + '1234abcd'+ NL + COLOR_GREEN + MOVE_RIGHT_IN + MOVE_RIGHT_OUT + SPEED_SLOW + Font.n14x8 + 'EFGH6789' + NL + MOVE_LEFT_IN + MOVE_LEFT_OUT + SPEED_FASTEST + COLOR_AMBER + Font.n5x5 + 'IJKL0123' + CODA
print str(data)

ser = serial.Serial(port, baudRate)
x = ser.write(data)
ser.close()


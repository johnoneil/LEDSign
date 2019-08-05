#!/usr/bin/env python
# vim: set ts=2 expandtab:

'''
Write a text file using v2.0 protocol with checksum
v2.0 supports filenames up to 12 characters
'''

import serial
from JetFileII import Message
from JetFileII import TextFile


file = TextFile('{pause=5}{middle}{moveRightIn}{moveLeftOut}{b16x12}{green}{hhmin_12hr}{nl}{amber}{7x6}{dow_abbr}, {month_abbr} {date} {yyyy}', "AB.nmg", drive='D')


#port = '/dev/ttyS0'
port = '/dev/ttyUSB0'
#port = '/dev/ttyACM0'

baudRate = 19200
ser = serial.Serial(port, baudRate)
x = ser.write(Message.WriteTextFilewithChecksum(file))
ser.close()

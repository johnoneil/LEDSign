#!/usr/bin/python
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
from JetFileIIProtocol import Message

msgs = []
msgs.append( Message.File('WEATHER',file_label='WEATHER.TXT') )
msgs.append( Message.File('NEWS',file_label='NEWS.TXT') )
msgs.append( Message.File('SPORTS',file_label='SPORTS.TXT') )

playlist = Message.WriteSystemFile(Message.Playlist(msgs))

print "Playlist is: " + playlist.encode('hex')
print playlist

port = '/dev/ttyS0'
baudRate = 19200
ser = serial.Serial(port, baudRate)

x = ser.write(playlist)

for msg in msgs:
  print msg.data.encode("hex")
  x = ser.write(msg.data)


ser.close()


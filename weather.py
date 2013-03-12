#!/usr/bin/python
# vim: set ts=2 expandtab:

#******************************************************************************
#
# weather.py
# John O'Neil
# Monday, March 11th, 2013
#
# Fetch weather via pywapi (python weather api) draw data out of JSON
# and send it to my LED sign.
# This is a test in preparation for an integrated LED sign server type daemon
# that could have something like this as just one small dedicated 'process'.
#
# REQUIRES: debian package "python-pywapi" available in Ubuntu 12.04 or
# google code.
#
#******************************************************************************

import pywapi
import serial
from JetFileIIProtocol import Message
displayMsg = Message.DisplayControlWithoutChecksum

#fetch the weather forecast for a given zip code
zipcode = 'ZIP:89101'
weather = pywapi.get_weather_from_yahoo('89129')

import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(weather)


condition  = weather['condition']['text']
humidity = weather['atmosphere']['humidity']
temp = weather['condition']['temp']
wind = weather['wind']['speed']

text = '{amber}{7x6}{nonein}{noneout} Currently: {green}' +condition+'{nl}'
text = text + '{amber}Temp: {red}' + temp + ' degrees{nl}'
text = text + '{amber}Humidity: {green}' + humidity + '%{nl}'
text = text + '{amber}Wind: {red}' + humidity + '{nl}'

msg = displayMsg.Create(1,text=text);

port = '/dev/ttyS0'
baudRate = 19200
ser = serial.Serial(port, baudRate)
x = ser.write(msg)
ser.close()

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
import time
import datetime
from time import mktime
from datetime import datetime
from JetFileIIProtocol import Message
displayMsg = Message.DisplayControlWithoutChecksum

#fetch the weather forecast for a given zip code
zipcode = '89129'
weather = pywapi.get_weather_from_yahoo(zipcode)

import pprint
pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(weather)

def mps2mph(mps):
  return  mps * 2.23694
def celsius2farenheight( celsius ):
  return celsius * 1.8 + 32
condition  = weather['condition']['text']
humidity = weather['atmosphere']['humidity']
temp_celsius = float(weather['condition']['temp'])
temp = str( round(celsius2farenheight(temp_celsius),2))
wind_mps = float( weather['wind']['speed'] )
wind = str( round(mps2mph(wind_mps),2) )

date_1 = weather['forecasts'][0]['date']
date_2 = weather['forecasts'][1]['date']
time_1 = time.strftime("%a, %b %d",time.strptime(date_1, "%d %b %Y"))
time_2 = time.strftime("%a, %b %d",time.strptime(date_2, "%d %b %Y"))
#weekday_1 = datetime.fromtimestamp(mktime(time_1)).weekday()
print time_1 + " " +time_2
forecast_temp_low_1 = str(int(celsius2farenheight(float(weather['forecasts'][0]['low']))))
forecast_temp_high_1 = str(int(celsius2farenheight(float(weather['forecasts'][0]['high']))))
forecast_text_1 = weather['forecasts'][0]['text']
forecast_temp_low_2 = str(int(celsius2farenheight(float(weather['forecasts'][1]['low']))))
forecast_temp_high_2 = str(int(celsius2farenheight(float(weather['forecasts'][1]['high']))))
forecast_text_2 = weather['forecasts'][1]['text']

text = '{pause=10}{typesetOff}{fastest}{amber}{7x6}{moverightin}{moverightout}Currently: {green}' +condition+'{nl}'
text = text + '{amber}{moveleftin}{moveleftout}Temp: {red}' + temp + ' degrees{nl}'
text = text + '{amber}{moverightin}{moverightout}Humidity: {green}' + humidity + '%{nl}'
text = text + '{amber}{moveleftin}{moveleftout}Wind: {red}' + wind + 'mph{nl}'
text = text + '{newframe}{fastest}{amber}{7x6}{moveupin}{movedownout}Forecast:{nl}'
text = text + '{green}' + time_1 + '{nl}'
text = text + '{red}Low:' + forecast_temp_low_1 + ' High: ' +forecast_temp_high_1 + '{nl}'
text = text + '{amber}' + forecast_text_1 + '{nl}'
text = text + '{newframe}{fastest}{amber}{7x6}{movedownin}{moveupout}Forecast:{nl}'
text = text + '{green}' + time_2 + '{nl}'
text = text + '{red}Low:' + forecast_temp_low_2 + ' High: ' +forecast_temp_high_2 + '{nl}'
text = text + '{amber}' + forecast_text_2 + '{nl}'

msg = displayMsg.Create(1,text=text);

port = '/dev/ttyS0'
baudRate = 19200
ser = serial.Serial(port, baudRate)
x = ser.write(msg)
ser.close()

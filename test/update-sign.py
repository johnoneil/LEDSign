#!/usr/bin/env python
# vim: set ts=2 expandtab:

#******************************************************************************
# Update my sign with muh stuff
#******************************************************************************


import serial
from JetFileII import Message
from JetFileII import TextFile
from JetFileII import PictureFile
from JetFileII import SEQUENTSYS
displayMsg = Message.DisplayControlWithoutChecksum
import time

import requests 
import json
import feedparser
from weather import Weather, Unit

def generateTimeScreen():
  return TextFile('{pause=6}{middle}{nonein}{noneout}{b16x12}{green}{hhmin_12hr}{nl}{amber}{7x6}{dow_abbr}, {month_abbr} {date} {yyyy}', "AB.nmg", drive='D')


def generateWeatherFeed():
  # r1 = requests.get('https://api.weather.gov/points/36.1211,-115.3508')
  # json1 = r1.json()
  # location = json1['properties']['relativeLocation']['properties']
  # city = location['city']
  # state = location['state']
  # print("weather for " + city + ", " + state)
  # don't know if the following url is static, but we can find it via the code above
  r2 = requests.get('https://api.weather.gov/gridpoints/VEF/114,96/forecast')
  json2 = r2.json()
  f1 = json2['properties']['periods'][0]
  f1s = '{s1}{green}{time}: {amber}{red}{temp}{nl}{amber}{forecast}'.format(s1='{7x6}',green='{green}', red='{red}', time=f1["name"], amber='{amber}', temp=f1["temperature"], nl="{nl}", forecast=f1["shortForecast"])
  f2 = json2['properties']['periods'][1]
  f2s = '{s1}{green}{time}: {amber}{red}{temp}{nl}{amber}{forecast}'.format(s1='{7x6}',green='{green}', red='{red}', time=f2["name"], amber='{amber}', temp=f2["temperature"], nl="{nl}", forecast=f2["shortForecast"])
  #f3 = json2['properties']['periods'][2]
  #f3s = '{s1}{green}{time}: {amber}{red}{temp}{nl}{amber}{forecast}'.format(s1='{7x6}',green='{green}', red='{red}', time=f3["name"], amber='{amber}', temp=f3["temperature"], nl="{nl}", forecast=f3["shortForecast"])
  #print("Forecast: " + f1["name"] + " temp: " + str(one["temperature"]) + " forecast: " + one["shortForecast"])
  return TextFile('{pause=2}{randomin}{randomout}{fastest}%s{newframe}%s' % ( f1s, f2s ), "AW.nmg", drive='D')

def generateBTCScreen():
  r = requests.get('https://api.coinmarketcap.com/v2/ticker/1/')
  jsonObject = r.json()
  btcprice = int(jsonObject["data"]["quotes"]["USD"]["price"])
  percent_change_24h = float(jsonObject["data"]["quotes"]["USD"]["percent_change_24h"])
  percent_change_7d = float(jsonObject["data"]["quotes"]["USD"]["percent_change_7d"])
  color24 = '{green}'
  color7d = '{green}'
  if percent_change_24h < 0 :
    color24 = '{red}'
  if percent_change_7d < 0 :
    color7d = '{red}'
  change24 = '{color}{value:+.1f}'.format(color=color24, value=percent_change_24h)
  change7d = '{color}{value:+.1f}'.format(color=color7d, value=percent_change_7d)
  return TextFile('{wipeupwardin}{wipeupwardout}\x14DD{middle}%s{b16x12}{halfspace}$%s{nl}{7x6}{amber}BTC %sd %sw' % ( color24, '{:,d}'.format(btcprice), change24, change7d ), 'AC.nmg', drive='D')

def generateDrudgeFeed():
  d = feedparser.parse('http://drudgereportfeed.com/rss.xml')
  #print("drudge feed:")
  #print(d)
  try:
    h1 = d['entries'][0]['title'].decode("utf-8").encode("ascii","ignore").strip()
  except Exception as exception:
    h1 = "Headline 1 Error"
  try:
    h2 = d['entries'][1]['title'].decode("utf-8").encode("ascii","ignore").strip()
  except Exception as exception:
    h2 = "Headline 2 Error"
  try:
    h3 = d['entries'][2]['title'].decode("utf-8").encode("ascii","ignore").strip()
  except Exception as exception:
    h3 = "Headline 3 Error"
  return TextFile('{pause=0}{middle}{moveLeftIn}{moveLeftOut}{font3}{green}{typesetoff}DRUDGE REPORT: {amber}{7x6}%s %s %s' % (h1, h2, h3), "AD.nmg", drive='D')

files = []
if True:
  files.append(generateTimeScreen())
  #files.append(PictureFile('../images/awesome.bmp', 'sugoi.bmp', 'D'))
  files.append(generateWeatherFeed())
  files.append(generateBTCScreen())
  files.append(generateDrudgeFeed())
  #files.append(TextFile('{middle}{left}{green}{b16x12}$10,600', 'AC.nmg', drive='D'))


#port = '/dev/ttyUSB0'
#port = '/dev/ttyACM0'
port = '/dev/ttyVIRTUAL'
baudRate = 19200
ser = serial.Serial(port, baudRate)


# # upload an image used in a text file (inline, so label is ONE character)
# coinpic = PictureFile('../images/coins.bmp', 'D', 'D')
# for packetNumber in range(0,coinpic.numPackets):
#   print("Writing image " + coinpic.label + " do drive: " + coinpic.drive + " packet number: " + str(packetNumber))
#   ser.write(Message.WritePictureFileWithChecksum(coinpic, packetNumber=packetNumber))
#   time.sleep(1)

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

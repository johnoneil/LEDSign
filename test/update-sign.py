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

def generateTimeScreen():
  return TextFile('{pause=5}{middle}{moveRightIn}{moveRightOut}{b16x12}{green}{hhmin_12hr}{nl}{amber}{7x6}{dow_abbr}, {month_abbr} {date} {yyyy}', "AB.nmg", drive='D')


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


files = []
if True:
  files.append(generateTimeScreen())
  #files.append(PictureFile('../images/awesome.bmp', 'sugoi.bmp', 'D'))
  files.append(generateBTCScreen())
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

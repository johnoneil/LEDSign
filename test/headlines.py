#!/usr/bin/python
# vim: set ts=2 expandtab:

#******************************************************************************
#
# headlines.py
# John O'Neil
# Tuesday, March 12th 2013
#
# Fetch Wall Street Journal (or some other) news source and show headlines
# as traditional "times square" scrolling marquee.
#
#******************************************************************************

import serial
from JetFileII import Message
displayMsg = Message.DisplayControlWithoutChecksum

import feedparser
#url = 'http://news.google.com.br/news?pz=1&cf=all&ned=us&hl=en&output=rss' 
url = 'http://online.wsj.com/xml/rss/3_8068.xml'
# just some GNews feed - I'll use a specific search later
text = ''
#text = text + '{typeseton}{5x5}{nonein}{noneout}{top}{left}{red}Wall Street Journal{nl}'
text = text + '{typesetoff}{amber}{b16x12}{middle}{fastest}{moveleftin}{moveleftout}'
feed = feedparser.parse(url)
for post in feed.entries:
  text = text + post.title + ' {red}{5x5} *** WSJ U.S. News *** {b16x12}{amber}'
   #print post.title
   #print post.keys()



msg = displayMsg.Create(1,text=text);

port = '/dev/ttyS0'
baudRate = 19200
ser = serial.Serial(port, baudRate)
x = ser.write(msg)
ser.close()

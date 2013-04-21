#!/usr/bin/python
# vim: set ts=2 expandtab:
###############################################################################
#
# server.py
# John O'Neil
# Monday, April 1st 2013
#
# Simple server maintaining my chainzone LED sign (32x128)
#
###############################################################################

import sys
import daemon #python-daemon package
import time
import serial

from task import *
from pop3 import pop3EmailTask

class LEDSignServer(object):
  def __init__(self,port,baud_rate,user='',pw=''):
    self.port = serial.Serial(port, baud_rate)

    self.tasks = []
    self.tasks.append( WeatherTask(self) )
    self.tasks.append( TimeTask(self) )
    #self.tasks.append( NewsTask(self,file_label='NEWS1.TXT',url='http://online.wsj.com/xml/rss/3_8068.xml',num_stories=3) )
    #self.tasks.append( TimeTask(self) )
    #self.tasks.append( NewsTask(self,file_label='NEWS2.TXT',url='http://online.wsj.com/xml/rss/3_8068.xml',start_story=3,num_stories=3) )
    self.tasks.append( pop3EmailTask(self,user=user,pw=pw) )
    #self.tasks.append( NowPlayingTask(self) )

    #have those tasks that need to update the sign
    #with their textfiles (i.e. constantly cycled tasks)
    self.UploadTextFiles()
    
    #form a playlist from constantly cycled tasks
    #and upload it to server.
    self.UploadPlaylist()

  def UploadTextFiles(self):
    for task in self.tasks:
      task.UpdateText()

  def FormPlaylist(self):
    playlist_entries = []
    for task in self.tasks:
      new_entry = task.GeneratePlaylistEntry()
      if new_entry is not None:
        playlist_entries.append(new_entry)
    if playlist_entries:
      return Message.WriteSystemFile(Message.Playlist(playlist_entries))
    return None
      
  def UploadPlaylist(self):
    playlist = self.FormPlaylist()
    if playlist is not None:
      self.port.write(playlist)
      time.sleep(1)

  def SendMessage(self, msg):
    if(msg):
      self.port.write(msg)
      time.sleep(1)
 
  def Run(self):
    while(self.tasks):
      for task in self.tasks:
        task.Service()
      time.sleep(1)

def main():
  #with daemon.DaemonContext():
  if(len(sys.argv)<3):
    print "USAGE: server <imap user> <imap password>"
    sys.exit(0)

  user = sys.argv[1]
  pw = sys.argv[2]
  server = LEDSignServer(port='/dev/ttyS0', baud_rate=19200,user=user,pw=pw)
  server.Run() 

if __name__ == "__main__":
  main()

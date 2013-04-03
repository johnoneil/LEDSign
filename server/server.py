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

import daemon #python-daemon package
import time
import serial

from task import *

class LEDSignServer(object):
  def __init__(self,port,baud_rate):
    self.port = serial.Serial(port, baud_rate)

    self.tasks = []
    self.tasks.append( WeatherTask(self) )
    self.tasks.append( TimeTask(self) )
    #self.tasks.append( NewsTask(self) )
    #self.tasks.append( EmailCheckTask(self) )
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
  server = LEDSignServer(port='/dev/ttyS0', baud_rate=19200)
  server.Run() 

if __name__ == "__main__":
  main()

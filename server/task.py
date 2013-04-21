# vim: set ts=2 expandtab:
###############################################################################
#
# task.py
# John O'Neil
# Monday, April 1st 2013
#
# "interface" for generic tasks in LED sign server.
# Python is not well suited to this approach, but
#
###############################################################################

import time
from JetFileII import Message
import pywapi
import datetime
import feedparser

#"abstract" interface
class Task(object):
  #constructor has reference to parent server so
  #we can call the led_sign_server.SendMessage() method on it
  def __init__(self, led_sign_server):
    pass
  #Update a text file on the LED sign via the passed serial port
  def UpdateText(self, port):
    raise NotImplementedError
  #generate an entry which can be used by clients to generate a
  #complete LED sign playlist
  def GeneratePlaylistEntry(self):
    raise NotImplementedError
  #service the running of the task. It's up to the task
  #to implement timestamping or make some other determination
  #for when it ought to do things
  def Service(self):
    raise NotImplementedError

class TimeTask(Task):
  def __init__(self, led_sign_server):
    self.led_sign = led_sign_server
    self.update_interval = 60 * 60 * 24 #update timme once per day in seconds
    self.last_update = None
    self.message = '{pause=10}{fastest}{middle}{center}{movedownin}{moveupout}{7x6}{amber}{dow_abbr}{month_abbr} {date},{yyyy}{nl}{22x18}{moveupin}{movedownout}{green}{hhmin_12hr}'
    self.partition = 'E'
    self.file_label = 'TIME.TXT'
  def Service(self):
    if(self.last_update is None):
      self.last_update = time.time()
    current_time = time.time()
    elapsed_time = current_time - self.last_update
    if( elapsed_time >= self.update_interval ):
      update_time_msg = Message.SetSystemTime()
      self.led_sign.SendMessage(update_time_msg)
      time.sleep(1)
      screen_msg = self.UpdateText()
      self.led_sign.SendMessage(screen_msg)
      time.sleep(1)
      self.last_update = current_time
  def UpdateText(self):
    msg = Message.WriteText(self.message,disk_partition=self.partition,file_label=self.file_label)
    self.led_sign.SendMessage(msg)
    time.sleep(1)
  def GeneratePlaylistEntry(self):
    return Message.File(self.message,file_label=self.file_label,partition=self.partition)

class WeatherTask(Task):
  def __init__(self, led_sign_server):
    self.led_sign = led_sign_server
    self.update_interval = 60 * 60 #update once every hour
    self.last_update = None
    self.partition = 'E'
    self.file_label = 'WEATHER.TXT'
    self.text = ''

  def mps2mph(self,mps):
    return  mps * 2.23694
  def celsius2farenheight(self,celsius ):
    return celsius * 1.8 + 32
  def Service(self):
    if(self.last_update is None):
      self.last_update = time.time()
    current_time = time.time()
    elapsed_time = current_time - self.last_update
    if( elapsed_time >= self.update_interval ):
      screen_msg = self.UpdateText()
      self.led_sign.SendMessage(screen_msg)
      time.sleep(1)
      self.last_update = current_time
  def GenerateWeatherConditionsText(self):
    zipcode = '89129'
    weather = pywapi.get_weather_from_yahoo(zipcode)
    condition  = weather['condition']['text'].encode('UTF-8')
    humidity = weather['atmosphere']['humidity'].encode('UTF-8')
    temp_celsius = float(weather['condition']['temp'])
    temp = str( round(self.celsius2farenheight(temp_celsius),2)).encode('UTF-8')
    wind_mps = float( weather['wind']['speed'] )
    wind = str( round(self.mps2mph(wind_mps),2) ).encode('UTF-8')

    date_1 = weather['forecasts'][0]['date']
    date_2 = weather['forecasts'][1]['date']
    time_1 = time.strftime("%a, %b %d",time.strptime(date_1, "%d %b %Y")).encode('UTF-8')
    time_2 = time.strftime("%a, %b %d",time.strptime(date_2, "%d %b %Y")).encode('UTF-8')
    forecast_temp_low_1 = str(int(self.celsius2farenheight(float(weather['forecasts'][0]['low'])))).encode('UTF-8')
    forecast_temp_high_1 = str(int(self.celsius2farenheight(float(weather['forecasts'][0]['high'])))).encode('UTF-8')
    forecast_text_1 = weather['forecasts'][0]['text'].encode('UTF-8')
    forecast_temp_low_2 = str(int(self.celsius2farenheight(float(weather['forecasts'][1]['low'])))).encode('UTF-8')
    forecast_temp_high_2 = str(int(self.celsius2farenheight(float(weather['forecasts'][1]['high'])))).encode('UTF-8')
    forecast_text_2 = weather['forecasts'][1]['text'].encode('UTF-8')

    text = '{pause=5}{typesetOff}{fastest}{amber}{5x5}{moverightin}{moverightout}today: {7x6}{green}' + condition.encode('UTF-8') +'{nl}'
    text = text + '{5x5}{amber}{moveleftin}{moveleftout}Temp: {red}{7x6}' + temp + ' degrees{nl}'
    text = text + '{5x5}{amber}{moverightin}{moverightout}Humidity: {green}{7x6}' + humidity + '%{nl}'
    text = text + '{5x5}{amber}{moveleftin}{moveleftout}Wind: {red}{7x6}' + wind + 'mph{nl}'
    text = text + '{newframe}{fastest}{amber}{7x6}{moveupin}{movedownout}Forecast:{nl}'
    text = text + '{green}' + time_1 + '{nl}'
    text = text + '{red}Low:' + forecast_temp_low_1 + ' High: ' +forecast_temp_high_1 + '{nl}'
    text = text + '{amber}' + forecast_text_1 + '{nl}'
    text = text + '{newframe}{fastest}{amber}{7x6}{movedownin}{moveupout}Forecast:{nl}'
    text = text + '{green}' + time_2 + '{nl}'
    text = text + '{red}Low:' + forecast_temp_low_2 + ' High: ' +forecast_temp_high_2 + '{nl}'
    text = text + '{amber}' + forecast_text_2 + '{nl}'
    return text

  def UpdateText(self):
    text = self.GenerateWeatherConditionsText()
    if self.text != text:
      self.text = text
      msg = Message.WriteText(self.text,disk_partition=self.partition,file_label=self.file_label)
      self.led_sign.SendMessage(msg)
      time.sleep(1)
  def GeneratePlaylistEntry(self):
    return Message.File(self.text,file_label=self.file_label,partition=self.partition)


class NewsTask(Task):
  def __init__(self, led_sign_server,file_label='NEWS.TXT',url=None,start_story=0,num_stories=3):
    self.url = url
    self.start_story = start_story
    self.num_stories = num_stories
    self.led_sign = led_sign_server
    self.update_interval = 60 * 60 #update once every hour
    self.last_update = None
    self.partition = 'E'
    self.file_label = file_label
    self.text = ''

  def Service(self):
    if(self.last_update is None):
      self.last_update = time.time()
    current_time = time.time()
    elapsed_time = current_time - self.last_update
    if( elapsed_time >= self.update_interval ):
      screen_msg = self.UpdateText()
      self.led_sign.SendMessage(screen_msg)
      time.sleep(1)
      self.last_update = current_time
  def GenerateNewsText(self):
    #url = 'http://news.google.com.br/news?pz=1&cf=all&ned=us&hl=en&output=rss' 
    #url = 'http://online.wsj.com/xml/rss/3_8068.xml'
    if self.url is None:
      return 'No news url provided'
    text = ''
    #text = text + '{typeseton}{5x5}{nonein}{noneout}{top}{left}{red}Wall Street Journal{nl}'
    text = text + '{typesetoff}{amber}{b16x12}{middle}{fastest}{moveleftin}{moveleftout}'
    feed = feedparser.parse(self.url)
    for post in feed.entries[self.start_story:self.start_story+self.num_stories]:
      text = text + post.title.encode('UTF-8') + ' {red}{5x5} *** WSJ U.S. News *** {b16x12}{amber}'
    return text

  def UpdateText(self):
    text = self.GenerateNewsText()
    if self.text != text:
      self.text = text
      msg = Message.WriteText(self.text,disk_partition=self.partition,file_label=self.file_label)
      self.led_sign.SendMessage(msg)
      time.sleep(1)
  def GeneratePlaylistEntry(self):
    return Message.File(self.text,file_label=self.file_label,partition=self.partition)
  

    



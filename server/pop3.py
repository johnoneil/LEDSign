# vim: set ts=2 expandtab:
###############################################################################
#
# pop3.py
# John O'Neil
# Saturday, April 6th, 2013
#
# LED sign server task to check pop3 based email (e.g. gmail etc)
# and provide sign intermittent messages when new emails arrive
#
###############################################################################

import time
from JetFileII import Message
from task import Task
import email, getpass, os, datetime
import poplib
import time
from email import parser


class pop3EmailTask(Task):
  def __init__(self, led_sign_server,user='',pw='',pop3_server='pop.gmail.com', port=995):
    self.led_sign = led_sign_server
    self.update_interval = 30 #check for messages once every two minutes
    self.email_queue_interval = 15 #space email messages to the screen by 15 seconds
    self.last_update = None
    self.last_email_update = None
    self.message = '{pause=10}{fastest}{middle}{center}{movedownin}{moveupout}{7x6}{amber}{dow_abbr}{month_abbr} {date},{yyyy}{nl}{22x18}{moveupin}{movedownout}{green}{hhmin_12hr}'
    self.partition = 'E'
    self.email_queue = []
    self.user = user
    self.pw = pw
    self.pop3_server = pop3_server
    self.port = port
    
    #self.file_label = 'TIME.TXT'
  def Service(self):
    if(self.last_update is None):
      self.last_update = time.time()
    if(self.last_email_update is None):
      self.last_email_update = time.time()
    current_time = time.time()
    elapsed_time = current_time - self.last_update
    if( elapsed_time >= self.update_interval ):
      self.CheckEmail()
      self.last_update = current_time
    #if we've got pending email messages, send them to our LED screen
    elapsed_email_time = current_time - self.last_email_update
    if(self.email_queue and elapsed_email_time > self.email_queue_interval):
      msg = self.email_queue.pop(0)
      self.led_sign.SendMessage(msg)
      self.last_email_update = current_time
  def UpdateText(self):
    pass
  def GeneratePlaylistEntry(self):
    pass
  def CheckEmail(self):
    pop3 = poplib.POP3_SSL(self.pop3_server,self.port)
    pop3.user(self.user)
    pop3.pass_(self.pw)
    messages = [pop3.retr(i) for i in range(1, len(pop3.list()[1]) + 1)]
    # Concat message pieces:
    messages = ["\n".join(mssg[1]) for mssg in messages]
    #Parse message intom an email object:
    messages = [parser.Parser().parsestr(mssg) for mssg in messages]
    for message in messages:
      subject = message['subject']
      sender = message['from']
      msg = '{nonein}{noneout}{red}{7x6}{flashon}Email from:{flashoff}'
      msg = msg + '{nl}{amber}'+ sender + '{nl}{nonein}{noneout}{flashon}{green}subj:{flashoff}{amber}' + subject
      #print msg
      self.email_queue.append( Message.EmergencyMessage(msg,t=25) )
    pop3.quit()


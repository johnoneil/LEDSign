# vim: set ts=2 expandtab:
#******************************************************************************
#
# JetFileIIProtocol.py
# John O'Neil
# Saturday, March 9th 2013
#
# (simplified)JetfileII LED sign protocol derived off documentation
#
#******************************************************************************

import sys
import re
from struct import *
from time import localtime

class Animate:
  class Speed:
    Fastest = '\x0f0'
    VeryFast = '\x0f1'
    Fast = '\x0f2'
    Medium = '\x0f3'
    Slow = '\x0f4'
    VerySlow = '\x0f5'
    Slowest = '\x0f6'
  class Random:
    In = '\x0aI\x2f'
    Out = '\x0aO\x2f'
  class Jump:#'Jump' is really no "no animation" but None is a reserved keyword, so keeping 'jump'.
    In = '\x0aI\x30'
    Out = jump = '\x0aO\x30'
  class MoveLeft:
    In = '\x0aI\x31'
    Out = '\x0aO\x31'
  class MoveRight:
    In = '\x0aI\x32'
    Out = '\x0aO\x32'
  class WipeLeft:#called "scroll left" in documentation, but is really a wipe
    In = '\x0aI\x33'
    Out = '\x0aO\x33'
  class WipeRight:#called "scroll right" in documentation, but is really a wipe
    In = '\x0aI\x34'
    Out = '\x0aO\x34'
  class MoveUp:
    In = '\x0aI\x35'
    Out = '\x0aO\x35'
  class MoveDown:
    In = '\x0aI\x36'
    Out = '\x0aO\x36'
  class WipeHorizontalFromCenter:
    In = '\x0aI\x37'
    Out = '\x0aO\x37'
  class WipeUpward:
    In = '\x0aI\x38'
    Out = '\x0aO\x38'
  class WipeDownward:
    In = '\x0aI\x39'
    Out = '\x0aO\x39'
  class WipeHorizontalToCenter:
    In = '\x0aI\x3a'
    Out = '\x0aO\x3a'
  class WipeVerticalFromCenter:
    In = '\x0aI\x3b'
    Out = '\x0aO\x3b'
  class WipeVerticalToCenter:
    In = '\x0aI\x3c'
    Out = '\x0aO\x3c'
  class ShuttleFromLeftRight:
    In = '\x0aI\x3d'
    Out = '\x0aO\x3d'
  class ShuttleFromUpDown:
    In = '\x0aI\x3e'
    Out = '\x0aO\x3e'
  class PeelOffLeft:
    In = '\x0aI\x3f'
    Out = '\x0aO\x3f'
  class PeelOfRight:
    In = '\x0aI\x40'
    Out = '\x0aO\x40'
  class ShutterFromUpDown:
    In = '\x0aI\x41'
    Out = '\x0aO\x41'
  class ShutterFromLeftRight:
    In = '\x0aI\x42'
    Out = '\x0aO\x42'
  class Raindrops:
    In = '\x0aI\x43'
    Out = '\x0aO\x43'
  class RandomMosaic:
    In = '\x0aI\x44'
    Out = '\x0aO\x44'
  class TwinklingStars:
    In = '\x0aI\x45'
    Out = '\x0aO\x45'
  class HipHop:
    In = '\x0aI\x46'
    Out = '\x0aO\x46'
  class Radar:
    In = '\x0aI\x47'
    Out = '\x0aO\x47'
  class ToFourSides:
    In = '\x0aI\x34'
    Out = '\x0aO\x34'
  class FromFourSides:
    In = '\x0aI\x34'
    Out = '\x0aO\x34'
  class WipeOutFromFourBlocks:
    In = '\x0aI\x34'
    Out = '\x0aO\x34'
  class MoveOutFromFourBlocks:
    In = '\x0aI\x54'
    Out = '\x0aO\x54'
  class MoveInToFourBlocks:
    In = '\x0aI\x53'
    Out = '\x0aO\x53'
  class WipeFromULSquare:
    In = '\x0aI\x54'
    Out = '\x0aO\x54'
  class WipeFromLRSquare:
    In = '\x0aI\x55'
    Out = '\x0aO\x55'
  class WipeFromULSquare:
    In = '\x0aI\x56'
    Out = '\x0aO\x56'
  class WipeFromURSquare:
    In = '\x0aI\x57'
    Out = '\x0aO\x57'
  class WipeFromULSlant:
    In = '\x0aI\x58'
    Out = '\x0aO\x58'
  class WipeFromURSlant:
    In = '\x0aI\x59'
    Out = '\x0aO\x59'
  class WipeFromLLSlant:
    In = '\x0aI\x5a'
    Out = '\x0aO\x5a'
  class WipeFromLRSlant:
    In = '\x0aI\x5b'
    Out = '\x0aO\x5b'
  class MoveInFromULCorner:
    In = '\x0aI\x5c'
    Out = '\x0aO\x5c'
  class MoveInFromURCorner:
    In = '\x0aI\x5d'
    Out = '\x0aO\x5d'
  class MoveInFromLLCorner:
    In = '\x0aI\x5e'
    Out = '\x0aO\x5e'
  class MoveInFromLRCorner:
    In = '\x0aI\x5f'
    Out = '\x0aO\x5f'
  class GrowingUp:
    In = '\x0aI\x60'
    Out = '\x0aO\x60'
  
  class Pause:
    @staticmethod
    def Seconds(seconds):
      sec = int(seconds)
      #TODO: Better handling of seconds values greater than 99
      return '\x0e0{0:02d}'.format(sec)

class Format:
  NewFrame = '\x0c'
  NewLine = '\x0d'
  Halfspace = '\x82'
  class Temperature:
    Celsius = '\x0b\x31'
    Farenheit = '\x0b\x33'
    Humidity = '\x0b\x32'
  @staticmethod
  def Linespace(space):
    if space<0 or space > 9:
      return Linespace(0)
    else:
      return '\x08' + str(space)
  class Flash:
    On = '\x071'
    Off = '\x070'
  class AutoTypeset:
    Off = '\x1b0a'
    On = '\x1b0b'
  class Background:
    Black = '\x1d0'
    Red = '\x1d1'
    Green = '\x1d2'
    Amber = '\x1d3'
  class Align:
    class Vertical:
      Center = '\x1f0'
      Top = '\x1f1'
      Bottom = '\x1f2'
    class Horizontal:
      Center = '\x1e0'
      Left = '\x1e1'
      Right = '\x1e2'
  @staticmethod
  def InterpretMarkup(text):
    #replace entries in curly brackets by their proper protocol values
    #e.g. 'hello {Format.NewLine} There' will insert Format.NewLine binary in place of curly brackets markup.
    def ReplaceMarkupTagWithArg(match):
      code = match.group(1).strip().lower()
      arg = match.group(2).strip().lower().split(',')
      #print "code: " + code +" arg: " + arg
      if(len(arg) == 1):
        arg = arg[0]
      if code in Markup.Registry:
        #pass
        return Markup.Registry[code](arg)
      return match.group(0)
    def ReplaceMarkupTags(match):
      code = match.group(1).strip().lower()
      #print "code is " + code
      if code in Markup.Registry:
          return Markup.Registry[code]
      return match.group(0)
    
    regex_with_arg = re.compile(r"\{(.*?)=(.*?)\}")
    regex = re.compile(r"\{(.*?)\}")
    text = re.sub(regex_with_arg, ReplaceMarkupTagWithArg, text)
    text = re.sub(regex, ReplaceMarkupTags, text)
    #print "subbed text: " + text
    return text

class Date:
  class MMDDYY:
    WithForwardSlashes = '\x0b\x20'
    WithDashes = '\x0b\x22'
    WithDots = '\x0b\x24'
  class DDMMYY:
    WithForwardSlashes = '\x0b\x21'
    WithDashes = '\x0b\x23'
  YY = '\x0b\x25'
  YYYY = '\x0b\x26'
  class Month:
    Number = '\x0b\x27'
    Abbreviation = '\x0b\x28'
  Day = '\x0b\x29'#day of month as two digit number
  class DayOfWeek:
    Number = '\x0b\x2a'
    Abbreviation = '\x0b\x2b'
  class Time:
    HH = '\x0b\x2c'
    MIN = '\x0b\x2d'
    SEC = '\x0b\x2e'
    HHMIN23hr = '\x0b\x2f'
    HHMIN12hr = '\x0b\x30'

#picture handling is described in protocol section 4
class Picture:
  @staticmethod
  def FromDiskFilename(filename,disk='E'):
    return '\x14'+disk+filename
  

class Font:
  n5x5 = '\x1a0' # C:\FONT\NORMAL5.FNT
  n7x6 = '\x1a1' # C:\FONT\NORMAL7.FNT
  n14x8 = '\x1a2' # C:\FONT\NORMAL14.FNT
  n15x9 = '\x1a3' # C:\FONT\NORMAL15.FNT
  n16x9 = '\x1a4' # C:\FONT\NORMAL16.FNT
  n24x16 = '\x1a6' # C:\FONT\NORMAL24.FNT
  n32x18 = '\x1a8' # C:\FONT\NORMAL32.FNT
  n11x9 = '\x1a:' # C:\FONT\NORMAL11.FNT
  n12x7 = '\x1a;' # LACKING
  n22x18 = '\x1a<' # C:\FONT\NORMAL22.FNT
  n30x18 = '\x1a=' # C:\FONT\NORMAL30.FNT
  n40x21 = '\x1a>' # C:\FONT\NORMAL40.FNT
  b14x10 = '\x1aN' # C:\FONT\BOLD14.FNT
  b15x10 = '\x1aO' # C:\FONT\BOLD15.FNT
  b16x12 = '\x1aP' # C:\FONT\BOLD16.FNT
  b24x8 = '\x1aQ' # LACKING
  b32x8 ='\x1aR' # LACKING
  b11x7 = '\x1aS' # LACKING
  b12x7 = '\x1aT' # LACKING
  b22x12 = '\x1aU' # LACKING
  b40x21 = '\x1aV' # LACKING
  class Color:
    Black = '\x1c\x30'
    Red = '\x1c\x31'
    Green = '\x1c\x32'
    Amber = '\x1c\x33'

    @staticmethod
    def CustomBGR(bgr):
      b = min(int(bgr[0]) , 255)
      g = min(int(bgr[1]) , 255)
      r = min(int(bgr[2]) , 255)
      return "\x1C\x2F" + pack("BBB" , b,g,r)
    @staticmethod
    def CustomRGB(rgb):
      return Font.Color.CustomBGR([rgb[2] , rgb[1] , rgb[0]])

    class Mixed:
      Characters = '\x1c\x34'
      Horizontal = '\x1c\x35'
      Wave = '\x1c\x36'
      Splash = '\x1c\x37'

class TextFile(object):
  def __init__(self, txt, label, drive='D'):
    t = Format.InterpretMarkup(txt)
    self.data = '\x01Z00\x02AA' + t + '\x04'
    self.type = 'T'
    self.label = label
    self.drive = drive

class PictureFile(object):
  def __init__(self, file, label, drive='D'):
    with open(file, mode='rb') as file:
      self.data = file.read()
    self.label = label
    self.type = 'P'
    self.drive = drive
    # limit to max packet size of 768 bytes (though true limit should be 1024)
    self.numPackets = int(len(self.data) / 768) + 1

# SEQUENT.SYS (playlist) format
def SEQUENTSYS(files):
  m = 'SQ'
  m = m + '\x04' # type
  m = m + '\x00' # valid
  m = m + pack('H', len(files)) # num files in list
  m = m + '\x00\x00' # reserved
  for f in files:
    m = m + f.drive # drive e.g. 'D' or 'E'
    m = m + f.type # file type e.g. 'T' for text
    m = m + '\x0f' # use bafile_name field below
    m = m + '\x80' # week repetition, ignore
    # begin time (currently always ignored)
    m = m + Message.DateTimeStructure(year=2008,month=3,day=16,hour=0,minute=0)
    # send time (currently always ignored)
    m = m + Message.DateTimeStructure(year=2008,month=3,day=16,hour=0,minute=0)
    m = m + Message.Checksum(f.data) # 2 bytes: checksum of file
    m = m + pack('H', len(f.data)) # 2 bytes: file size
    m = m + Message.FileLabel(f.label) # filename padded to 12 bytes
  return m

#See section 3.1 of protocol description
class Message:
  Header = '\x00\x00\x00\x00\x00\x01Z00'
  Type2Header = 'QZ00SAX'
  Protocol = '\x06'
  BeginCommand = '\x02'
  WriteFile = 'A'
  Coda = '\x04'
  SYN = '\x55\xa7'
  class DisplayControlWithoutChecksum:
    @staticmethod
    def Create(msgId, unit_address=0, disk='E', folder='T', text='Testing, 1, 2, 3.'):
      p = Message.DisplayControlWithoutChecksum
      f = Format
      m = Message
      return m.Header + m.BeginCommand + m.WriteFile + m.MsgId2DiskFolderFilename(msgId,disk=disk,folder=folder) + m.Protocol + f.InterpretMarkup(text) + m.Coda
  @staticmethod
  def MsgId2Filename(msgId, fileType='T'):
    """
    In JetFileII, with or without checksum filenames are limted to 2 characters.
    So if the msgID is not a string of two characters, it will interpret
    a single integer value as a 2 character string
    """
    if fileType != 'T':
      #picture filename can only be ONE character
      # see Appendix 1 Comparison Table for Valid File Labels and Value
      return str('%c' % (65 + int(msgId / 26)))
    else:
      if type(msgId) is str:
        msgId = msgId[:2]
        return msgId
      else:
        #asciiMajor = 65 + int(msgId/26)
        #asciiMinor = 65 + int(msgId % 26)
        #return '{0:01c}{0:01c}'.format(asciiMajor,asciiMinor)
        return str('%c%c' % (65 + int(msgId / 26), 65 + (msgId % 26)))
  
  
  @staticmethod
  def MsgId2DiskFolderFilename(msgId,disk='E',folder='T'):
    #print "MsgId2DiskFolderFilename returns filename " + Message.MsgId2Filename(msgId)
    return '\x0f' + disk + folder + Message.MsgId2Filename(msgId, fileType=folder)

  @staticmethod
  def Checksum(message):
    sum = 0
    USHRT_MAX = 65535
    for c in message:
      sum = (sum + ord(c)) & 0xffff
    sum = sum % USHRT_MAX
    packed =  pack('H',sum)
    return packed

  @staticmethod
  def Create(msg):
    return Message.Type2Header + Format.InterpretMarkup(msg) + Message.Coda
    #return Message.Type2Header + msg + Message.Coda

  @staticmethod
  def FileLabel(label):
    l = len(label.encode('utf-8'))
    if(l < 12):
      newlabel = label.ljust(12,'\x00')
      return newlabel
    elif (l > 12):
      return label[:12]
    return label

  @staticmethod
  def WriteText(message,disk_partition='E',buzzer_time=0,file_label='AB'):
    #build and return an emergency message with checksum backwards from data
    m = Message.Create(message)
    data_length = len(m)
    m = pack('I',data_length) +  pack('H',data_length) + pack('H',1) + pack('H',1) + m
    m = disk_partition + pack('B',buzzer_time) + Message.FileLabel(file_label) + m
    m = '\x00' + m;#flag
    m = '\x06' + m;#arglength (arg is 1x4 bytes long)
    m = '\x04' + m;#subcommand
    m = '\x02' + m;#main command
    m = '\xab\xcd' + m;#packet serial
    m = '\x00' + m;#source, dest addresses.
    m = '\x00' + m;
    m = '\x00' + m;
    m = '\x00' + m;
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  @staticmethod
  def getSystemFile(file_label='SEQUENT.SYS'):
    """
    Get system file as per (2).Read System Files (0x0102)
    JetFileIIv2.8.7_EN
    """
    data_length = 0
    m = '' # no data
    m = '\x00\x00' + m # packet size (?)
    m = '\x00\x01' + m # packet serial number (?) counted from 1
    m = Message.FileLabel(file_label) + m
    m = '\x01' + m;#flag
    m = '\x04' + m;#arglength (arg is 1x4 bytes long)
    m = '\x02' + m;#subcommand
    m = '\x01' + m;#main command
    m = '\xab\xcd' + m;#packet serial
    m = '\x00' + m; # dest address
    m = '\x00' + m; # source address
    m = pack('H',data_length) + m; # data len
    m = Message.Checksum(m) + m; # checksum
    m = Message.SYN + m; # sync
    return m

  @staticmethod
  def WriteSystemFile(file, file_label='SEQUENT.SYS'):
    #build and return an emergency message with checksum backwards from data
    m = file
    data_length = len(file)
    m = '\x00\x00' + m # 2 bytes: Note
    m = pack('H', 1) + m # current packet. from 0x01
    m = pack('H', 1) + m # number of packets
    m = '\x00\x03' + m # packet size REALLY unsure of correct values here
    m = pack('I', data_length) + m # 4 bytes total file size    
    m = Message.FileLabel(file_label) + m
    m = '\x00' + m; #flag x01 = 'in-echo' 0x00 = 'echo'
    m = '\x06' + m; #arglength (arg is 1x4 bytes long)
    m = '\x02' + m; #subcommand
    m = '\x02' + m; #main command
    m = '\xab\xcd' + m; # packet serial
    m = '\x01\x01' + m; # dest address
    m = '\x00\x00' + m; # source address
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = '\x55\xa7' + m;
    return m

  @staticmethod
  def SetSystemTime():
    data_length = 0
    current_time = localtime()
    year = int(str(current_time[0]),base=16)
    month = int(str(current_time[1]),base=16)
    day = int(str(current_time[2]),base=16)
    hour = int(str(current_time[3]),base=16)
    minute = int(str(current_time[4]),base=16)
    dow = int(str(current_time[6]),base=16)
    timezone = 0
    m = ''
    m = pack('H',year) + pack('B',month) + pack('B',day) + pack('B',hour) + pack('B',minute) + pack('B',dow) + pack('B',timezone) + m
    m = '\x00' + m;#flag
    m = '\x02' + m;#arglength (arg is 1x4 bytes long)
    m = '\x02' + m;#subcommand
    m = '\x05' + m;#main command
    m = '\xab\xcd' + m;#packet serial
    m = '\x00' + m;#source, dest addresses.
    m = '\x00' + m;
    m = '\x00' + m;
    m = '\x00' + m;
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  class TextFile:
    def __init__(self, data, msgId, disk='E', upload=True):
      #self.file_label=Message.FileLabel(file_label)
      #print "File label: " + self.file_label + " "+ self.file_label.encode('hex')
      #self.data=Message.WriteText(data,file_label=file_label,disk_partition=partition)
      self.data = Message.DisplayControlWithoutChecksum.Create(msgId,disk=disk,folder='T',text=data)
      self.file_label = Message.MsgId2Filename(msgId);
      self.longFileName = Message.FileLabel(self.file_label)
      self.filetype='T'
      self.disk = disk
      self.upload = upload
      self.fileSize = len(data)
      self.checksum = Message.Checksum(data)

    def path(self):
      return '\x0f' + self.disk + self.filetype + self.file_label

  @staticmethod
  def WriteTextFilewithChecksum(file):
    #build and return an emergency message with checksum backwards from data
    m = file.data
    data_length = len(file.data)
    m = '\x01\x00' + m
    m = '\x01\x00' + m
    m = '\x00\x03' + m # packet size REALLY unsure of correct values here
    m = pack('I', data_length) + m # file size (4 bytes)
    m = Message.FileLabel(file.label) + m
    m = '\x01' + m # buzzer ???
    m = file.drive + m
    m = '\x00' + m # 0x00 == echo ON
    m = '\x06' + m #arglength (arg is 1x4 bytes long)
    m = '\x04' + m #subcommand
    m = '\x02' + m #main command
    m = '\x4c\x00' + m #packet serial (just echoed in response)
    m = '\x01' + m
    m = '\x01' + m # dest address 1, 2 (0x01, 0x01)
    m = '\x00' + m
    m = '\x00' + m # source address 1, 2 (0,0)
    m = pack('H', data_length) + m
    m = Message.Checksum(m) + m
    m = Message.SYN + m
    return m

  @staticmethod
  def WritePictureFileWithChecksum(file, packetNumber=0):
    maxPacketSize = 768
    start = packetNumber * maxPacketSize
    packet = file.data[start:start+maxPacketSize]
    m = packet
    total_file_size = len(file.data)
    packet_size = len(packet)
    #print("the size of packet " + str(packetNumber) + " is: " + str(packet_size));
    m = pack('H', packetNumber + 1) + m # current packet(one based)
    m = pack('H', file.numPackets) + m # number of total packets
    m = '\x00\x03' + m # maximum packet size (768 bytes == 0x0300)
    m = pack('I', total_file_size) + m # file size (4 bytes)
    m = Message.FileLabel(file.label) + m
    m = '\x01' + m # reserved (docs say 0 but practice says 1)
    m = file.drive + m
    m = '\x00' + m # 0x00 == echo ON
    m = '\x06' + m # arglength (arg is 1x4 bytes long)
    m = '\x06' + m # subcommand
    m = '\x02' + m # main command
    m = '\xab\xcd' + m #packet serial (just echoed in response)
    m = '\x01\x01' + m # dest address
    m = '\x00\x00' + m # source address
    m = pack('H', packet_size) + m
    m = Message.Checksum(m) + m
    m = Message.SYN + m
    return m

  @staticmethod
  def ListFilesInFolder(drive='E', folder='T'):
    #build and return an emergency message with checksum backwards from data
    m = '' # no data

    filepath = 'E:\T\\x00'

    m = filepath + m

    m = '\x00' # flag: use designated path

    #m = '\x01' + m #arglength (arg is 1x4 bytes long)
    m = pack('B', (len(filepath) + 3) / 4)

    m = '\x0b' + m #subcommand
    m = '\x07' + m #main command
    m = '\xab\xcd' + m #packet serial
    m = '\x00\x00' + m # source addr
    m = '\x00\x00' + m # dest addresses.
    m = pack('H', 0) + m; # data length
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m


  @staticmethod
  def Playlist(files):
    """
    This is the simpler method of writing playlists (v1.0) that
    only supports filenames of max 2 characters. Works though.
    files is a list of objects that implement a 'path' member
    where path is returned in the form: '\x0fETAC'
    """
    m = ''
    m = m + '\x00\x00\x00\x00\x00\x01Z00'
    m = m + '\x02' # strt symbol of command
    m = m + 'E' # command code
    m = m + '.SL'
    for file in files:
      m = m + file.path() #'\x0fETAB'
    m = m + '\x03' # 0x04 = in-echo, 0x03 = echo
    return m

  @staticmethod
  def PlaylistFileFormat(files):
    #build and return an emergency message with checksum backwards from data
    num_files = len(files)
    m = 'SQ' + '\x04' + '\x00' + pack('H', num_files) + '\x00\x00'
    for file in files:
      m = m + file.disk + file.filetype + '\x0f' + Message.WeekRepetition()
      m = m + Message.DateTimeStructure(year=2008,month=3,day=16,hour=0,minute=0) # begin time
      m = m + Message.DateTimeStructure(year=2008,month=3,day=16,hour=0,minute=0) # send time
      m = m + Message.Checksum(file.data)
      m = m + pack('H',len(file.data))
      m = m + file.longFileName
      #m = m + pack('I', file.checksum) # checksum of file (UWORD)
    return m

  @staticmethod
  def StringFile(data, partition='E',file_label="string.txt"):
    #build and return an emergency message with checksum backwards from data
    messages = []
    data_size = len(data)
    num_messages = data_size/1024 + 1
    payload_size = data_size/num_messages
    for imsg in range(num_messages):
      m = data[imsg*payload_size:imsg*payload_size+payload_size] #Message.Create(message)
      data_length = len(m)
      m = partition + pack('B',0) +  Message.FileLabel(file_label) + pack('I',data_size) + pack('H',payload_size) + pack('H',num_messages) + pack('H',imsg+1) + m
      m = '\x00' + m;#flag
      m = '\x06' + m;#arglength (arg is 1x4 bytes long)
      m = '\x05' + m;#subcommand
      m = '\x02' + m;#main command
      m = '\xab\xcd' + m;#packet serial
      m = '\x00' + m;#source, dest addresses.
      m = '\x00' + m;
      m = '\x00' + m;
      m = '\x00' + m;
      m = pack('H',data_length) + m;
      m = Message.Checksum(m) + m;
      m = Message.SYN + m;
      if(num_messages is 1):
        return m
      messages.append(m)
    return messages   

  @staticmethod
  def UploadSmallPicture(data, partition='E', msgId=1):
    """
    v1 protocol to upload a picture up to 1024 bytes
    see Table2.3.1 on pg 19 of 205
    """
    m = ''
    m = m + '\x00\x00\x00\x00\x00\x01Z00'
    m = m + '\x02' # strt symbol of command
    m = m + 'I' # command code
    m = m + Message.MsgId2Filename(msgId,fileType='P') #'\x0fETAB'
    if data:
      m = m + data
    m = m + '\x03' # x04=in-echo x03=echo
    return m

  @staticmethod
  def UploadArrayPictures(data, width, height, numFrames, partition='E', msgId=1):
    """
    v1 protocol to upload an array of pictures, i.e. animation
    see Table7.1.1 Format of Array Picture File
    """
    m = ''
    m = m + '\x00\x00\x00\x00\x00\x01Z00'
    m = m + '\x02' # strt symbol of command
    m = m + 'CAPD' # command code
    #m = m + '\x01' # x01 = GR (16 bit 8:8 format)
    m = m + '\x00' # RGRGRGRG(2bit,1:1 format)
    m = m + '\x00' # not skip invalid display data in last frame
    m = m + pack('H', width)
    m = m + pack('H', height)
    m = m + pack('H', 2) # bits per point.
    m = m + pack('H', numFrames)
    m = m + pack('I', len(data))
    m = m + pack('I', len(data)/numFrames)
    m = m + pack('H', width) # last data width
    m = m + '\x00\x00' # reserved
    return m


  @staticmethod
  def ArrayAnimationFrame(imgData, width, height,):
    """
    Form header and body of single animation frame
    for use in uploading array type pictures
    """
    m = ''
    m = m + 'FH'
    if(height > 16):
      m = m + '\x00'
      m = m + '\x01'
    else:
      m = m + pack('H', height) # num rows in frame (max 16)
      m = m + '\x00'
    m = m + '' 

  @staticmethod
  def Picture(data, partition='E',file_label="AA"):
    """
    Build and return an array of strings, each string representing a single
    picture upload packet. This allows uploding windows bitmaps (Red/Green)
    representing pictures larger than 1024 bytes.
    """
    messages = []
    data_size = len(data)
    num_messages = data_size/512 + 1
    payload_size = data_size/num_messages
    for imsg in range(num_messages):
      m = data[imsg*payload_size:imsg*payload_size+payload_size]
      data_length = len(m)
      m = pack('H', imsg+1) + m # current packet, starting at 1 (2 bytes)
      m = pack('H',num_messages) + m # number of packets total (2 bytes)
      m = pack('H',payload_size) + m # size of  ll packets (2 bytes) all should be the same size
      m = pack('I',data_size) + m # total file size (2 bytes)
      m = Message.FileLabel(file_label) + m # file label (12 bytes, padded with \x00 if necessary)
      m = '\x00' + m # reserved, must be 'x00 (one byte)
      m = partition + m # partition (one byte)
      
      m = '\x00' + m; # flag 0x01 == 'in-echo' 0x00 == 'echo'
      m = '\x06' + m; # arglength (arg is 1x4 bytes long)
      m = '\x06' + m; # subcommand
      m = '\x02' + m; # main command
      m = '\xab\xcd' + m; # packet serial
      m = '\x00\x00' + m; # source address
      m = '\x00\x00' + m; # dest address
      m = pack('H',data_length) + m;
      m = Message.Checksum(m) + m;
      m = Message.SYN + m;
      #m = '\x00\x00\x00\x00\x00' + m
      messages.append(m)
    return messages   

  @staticmethod
  def DateTimeStructure(year=0,month=0,day=0,hour=0,minute=0):
    return pack('H',year) + pack('B',month) + pack('B',day) + pack('B',hour) + pack('B',minute) + '\x01' +'\x01'

  @staticmethod
  def WeekRepetition():
    return str('\x80')
  

  @staticmethod
  def EmergencyMessage(msg,t=10):
    #build and return an emergency message with checksum backwards from data
    m = TextFile(msg);
    data_length = len(m)
    m = pack('H',1) + '\x00' + '\x00' + m;#time, sound, reserved
    m = '\x01' + m;#flag
    m = '\x01' + m;#arglength (arg is 1x4 bytes long)
    m = '\x09' + m;#subcommand
    m = '\x02' + m;#main command
    m = '\xab\xcd' + m;#packet serial
    m = '\x01\x01' + m;#dest addresses.
    m = '\x00\x00' + m;#source address.
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  @staticmethod
  def TurnSignOff(goodbyeMsg=False):
    #build and return an emergency message with checksum backwards from data
    m = ''
    if goodbyeMsg:
      m = pack('I',0) + m
    else:
      m = pack('I',1) + m
    m = '\x00' + m; # flag (0x0 = ECHO)
    m = '\x01' + m; # arglength (fixed at 0x01)
    m = '\x03' + m; # subcommand
    m = '\x04' + m; # main command
    m = '\xab\xcd' + m; # packet serial
    m = '\x01\x01' + m; # dest addresses.
    m = '\x00\x00' + m; # source address
    m = pack('H',0) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  @staticmethod
  def TurnSignOn():
    #build and return an emergency message with checksum backwards from data
    m = ''
    m = '\x00' + m; # flag 0x00 == ECHO
    m = '\x00' + m; # arglength (arg is 1x4 bytes long)
    m = '\x04' + m; # subcommand
    m = '\x04' + m; # main command
    m = '\xab\xcd' + m; # packet serial
    m = '\x01\x01' + m; # dest addresses.
    m = '\x00\x00' + m; # source address
    m = pack('H',0) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  @staticmethod
  def AutoTest():
    """
    This command is used to make the LED sign test automatically (The test order: all
bright->all Red-> all Green->all Blue-> scan horizontally-> scan vertically>the basic
parameter of the sign)
    """
    m = ''
    data_length = 0
    m = '\x00' + m; # flag
    m = '\x00' + m; # arglength
    m = '\x02' + m; # subcommand = auto test (0x02)
    m = '\x03' + m; # main command = test command(0x03)
    m = '\xab\xcd' + m;#packet serial
    m = '\x00\x00' + m; # source addr
    m = '\x00\x00' + m; # dest addr
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  @staticmethod
  def StopTest():
    """ 
    This command is used to end the test on the LED sign. The format as the following
table:
    """
    m = ''
    data_length = 0
    m = '\x00' + m; # flag
    m = '\x00' + m; # arglength
    m = '\x09' + m; # subcommand = stop test (0x09)
    m = '\x03' + m; # main command = test command(0x03)
    m = '\xab\xcd' + m;#packet serial
    m = '\x00\x00' + m; # source addr
    m = '\x00\x00' + m; # dest addr
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  @staticmethod
  def StartCountdown(day=0,hour=0,minute=0,second=0):
    #build and return an emergency message with checksum backwards from data
    m = ''
    data_length = 0
    m = pack('B',day) + pack('B',hour) + pack('B',minute) + pack('B',second) + m
    m = '\x00' + m;#flag
    m = '\x01' + m;#arglength (arg is 1x4 bytes long)
    m = '\x11' + m;#subcommand
    m = '\x06' + m;#main command
    m = '\xab\xcd' + m;#packet serial
    m = '\x00' + m;#source, dest addresses.
    m = '\x00' + m;
    m = '\x00' + m;
    m = '\x00' + m;
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  @staticmethod
  def StopCountdown():
    #build and return an emergency message with checksum backwards from data
    m = ''
    data_length = 0
    m = '\x00' + m;#flag
    m = '\x00' + m;#arglength (arg is 1x4 bytes long)
    m = '\x12' + m;#subcommand
    m = '\x06' + m;#main command
    m = '\xab\xcd' + m;#packet serial
    m = '\x00' + m;#source, dest addresses.
    m = '\x00' + m;
    m = '\x00' + m;
    m = '\x00' + m;
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  @staticmethod
  def DynamicDisplay(ledData):
    #build and return an arra of messages (of same size)
    #that describe the display we want.
    #1 how many messages will we create?
    num_messages = len(ledData)/512
    data_length = 512
    message_array = []
    for iMsg in range(num_messages):
      start = iMsg*512
      end = start + 512
      m = ledData[start:end]
      m = pack('H', data_length) + pack('H',num_messages) + pack('H', iMsg+1) + pack('H',0) + m
      m = '\x00' + m;#flag
      m = '\x02' + m;#arglength (arg is 2x4 bytes long)
      m = '\x04' + m;#subcommand
      m = '\x08' + m;#main command
      m = '\xab\xcd' + m;#packet serial
      m = '\x00' + m;#source, dest addresses.
      m = '\x00' + m;
      m = '\x00' + m;
      m = '\x00' + m;
      m = pack('H',data_length) + m;
      m = Message.Checksum(m) + m;
      m = Message.SYN + m;
      message_array.append(m)
    return message_array

  class Bitmap:
    CommmandCharacter = 'I'
    @staticmethod
    def Create(filename,bytes,unit_address=0,disk='E'):
      p = Message.Bitmap
      f = Format
      m = Message
      return m.Header + m.BeginCommand + p.CommandCharacter + filename + bytes + m.Coda
 
#There's gotta be a better way than this...
class Markup:
  Registry = {
    'pause' : Animate.Pause.Seconds,
    'nl' : Format.NewLine,
    'newframe' : Format.NewFrame,
    'halfspace' : Format.Halfspace,
    'flashon' : Format.Flash.On,
    'flashoff' : Format.Flash.Off,
    'font_bgr': Font.Color.CustomBGR,
    'font_rgb': Font.Color.CustomRGB,
    'red' : Font.Color.Red,
    'green' : Font.Color.Green,
    'amber' : Font.Color.Amber,
    'top' : Format.Align.Vertical.Top,
    'middle' : Format.Align.Vertical.Center,
    'bottom' : Format.Align.Vertical.Bottom,
    'left' : Format.Align.Horizontal.Left,
    'center' : Format.Align.Horizontal.Center,
    'right' : Format.Align. Horizontal.Right,
    'typeseton' : Format.AutoTypeset.On,
    'typesetoff' : Format.AutoTypeset.Off,
    'slowest' : Animate.Speed.Slow,
    'veryslow' : Animate.Speed.VerySlow,
    'slow' : Animate.Speed.Slow,
    'medium' : Animate.Speed.Medium,
    'fast' : Animate.Speed.Fast,
    'veryFast' : Animate.Speed.VeryFast,
    'fastest' : Animate.Speed.Fastest,
    'nonein' : Animate.Jump.In,
    'noneout' : Animate.Jump.Out,
    'randomin' : Animate.Random.In,
    'randomout' : Animate.Random.Out,
    'moveleftin' : Animate.MoveLeft.In,
    'moveleftout' : Animate.MoveLeft.Out,
    'moverightin' : Animate.MoveRight.In,
    'moverightout' : Animate.MoveRight.Out,
    'wipeleftin' : Animate.WipeLeft.In,
    'wiperightin' : Animate.WipeRight.In,
    'moveupin' : Animate.MoveUp.In,
    'movedownin' : Animate.MoveDown.In,
    'wipehorizontalfromcenterin' : Animate.WipeHorizontalFromCenter.In,
    'wipeupwardin' : Animate.WipeUpward.In,
    'wipedownwardin' : Animate.WipeDownward.In,
    'wipehorizontaltocenterin' : Animate.WipeHorizontalToCenter.In,
    'wipeverticalfromcenterin' : Animate.WipeVerticalFromCenter.In,
    'wipeverticaltocenterin' : Animate.WipeVerticalToCenter.In,
    'shuttlefromleftrightin' : Animate.ShuttleFromLeftRight.In,
    'shuttlefromupdownin' : Animate.ShuttleFromUpDown.In,
    'peeloffleftin' : Animate.PeelOffLeft.In,
    'peeloffrightin' : Animate.PeelOfRight.In,
    'shutterfromupdownin' : Animate.ShutterFromUpDown.In,
    'shutterfromleftrightin' : Animate.ShutterFromLeftRight.In,
    'raindropsin' : Animate.Raindrops.In,
    'randommosaicin' : Animate.RandomMosaic.In,
    'twinklingstarsin' : Animate.TwinklingStars.In,
    'hiphopin' : Animate.HipHop.In,
    'radarin' : Animate.Radar.In,
    'tofoursidesin' : Animate.ToFourSides.In,
    'fromfoursidesin' : Animate.FromFourSides.In,
    'wipeoutfromfourblocksin' : Animate.WipeOutFromFourBlocks.In,
    'moveoutfromfourblocksin' : Animate.MoveOutFromFourBlocks.In,
    'moveintofourblocksin' : Animate.MoveInToFourBlocks.In,
    'wipefromulsquarein' : Animate.WipeFromULSquare.In,
    'wipefromlrsquarein' : Animate.WipeFromLRSquare.In,
    'wipefromulsquarein' : Animate.WipeFromULSquare.In,
    'wipefromursquarein' : Animate.WipeFromURSquare.In,
    'wipefromulslantin' : Animate.WipeFromULSlant.In,
    'wipefromurslantin' : Animate.WipeFromURSlant.In,
    'wipefromllslantin' : Animate.WipeFromLLSlant.In,
    'wipefromlrslantin' : Animate.WipeFromLRSlant.In,
    'moveinfromulcornerin' : Animate.MoveInFromULCorner.In,
    'moveinfromurcornerin' : Animate.MoveInFromURCorner.In,
    'moveinfromllcornerin' : Animate.MoveInFromLLCorner.In,
    'moveinfromlrcornerin' : Animate.MoveInFromLRCorner.In,
    'growingupout' : Animate.GrowingUp.In,
    'wipeleftout' : Animate.WipeLeft.In,
    'wiperightout' : Animate.WipeRight.Out,
    'moveupout' : Animate.MoveUp.Out,
    'movedownout' : Animate.MoveDown.Out,
    'wipehorizontalfromcenterout' : Animate.WipeHorizontalFromCenter.Out,
    'wipeupwardout' : Animate.WipeUpward.Out,
    'wipedownwardout' : Animate.WipeDownward.Out,
    'wipehorizontaltocenterout' : Animate.WipeHorizontalToCenter.Out,
    'wipeverticalfromcenterout' : Animate.WipeVerticalFromCenter.Out,
    'wipeverticaltocenterout' : Animate.WipeVerticalToCenter.Out,
    'shuttlefromleftrightout' : Animate.ShuttleFromLeftRight.Out,
    'shuttlefromupdownout' : Animate.ShuttleFromUpDown.Out,
    'peeloffleftout' : Animate.PeelOffLeft.Out,
    'peeloffrightout' : Animate.PeelOfRight.Out,
    'shutterfromupdownout' : Animate.ShutterFromUpDown.Out,
    'shutterfromleftrightout' : Animate.ShutterFromLeftRight.Out,
    'raindropsout' : Animate.Raindrops.Out,
    'randommosaicout' : Animate.RandomMosaic.Out,
    'twinklingstarsout' : Animate.TwinklingStars.Out,
    'hiphopout' : Animate.HipHop.Out,
    'radarout' : Animate.Radar.Out,
    'tofoursidesout' : Animate.ToFourSides.Out,
    'fromfoursidesout' : Animate.FromFourSides.Out,
    'wipeoutfromfourblocksout' : Animate.WipeOutFromFourBlocks.Out,
    'moveoutfromfourblocksout' : Animate.MoveOutFromFourBlocks.Out,
    'moveintofourblocksout' : Animate.MoveInToFourBlocks.Out,
    'wipefromulsquareout' : Animate.WipeFromULSquare.Out,
    'wipefromlrsquareout' : Animate.WipeFromLRSquare.Out,
    'wipefromulsquareout' : Animate.WipeFromULSquare.Out,
    'wipefromursquareout' : Animate.WipeFromURSquare.Out,
    'wipefromulslantout' : Animate.WipeFromULSlant.Out,
    'wipefromurslantout' : Animate.WipeFromURSlant.Out,
    'wipefromllslantout' : Animate.WipeFromLLSlant.Out,
    'wipefromlrslantout' : Animate.WipeFromLRSlant.Out,
    'moveinfromulcornerout' : Animate.MoveInFromULCorner.Out,
    'moveinfromurcornerout' : Animate.MoveInFromURCorner.Out,
    'moveinfromllcornerout' : Animate.MoveInFromLLCorner.Out,
    'moveinfromlrcornerout' : Animate.MoveInFromLRCorner.Out,
    'growingupout' : Animate.GrowingUp.Out,
    '5x5' : Font.n5x5,
    '7x6' : Font.n7x6,
    '14x8' : Font.n14x8,
    '15x9' : Font.n11x9,
    '16x9' : Font.n16x9,
    '24x16': Font.n24x16,
    '32x18': Font.n32x18,
    '11x9' : Font.n11x9,
    '22x18' : Font.n22x18,
    '30x18' : Font.n30x18,
    '40x21' : Font.n40x21,
    'b14x10':Font.b14x10,
    'b15x10':Font.b15x10,
    'b16x12':Font.b16x12,
    'font1' : '\x1aa',
    'font2' : '\x1ab',
    'font3' : '\x1ac',
    'font4' : '\x1ad',
    'font5' : '\x1ae',
    'font6' : '\x1af',
    'font7' : '\x1ag',
    'font8' : '\x1ah',
    'font9' : '\x1ai',
    'mm/dd/yy':Date.MMDDYY.WithForwardSlashes,
    'mm-dd-yy':Date.MMDDYY.WithDashes,
    'mm.dd.yy':Date.MMDDYY.WithDots,
    'dd/mm/yy':Date.DDMMYY.WithForwardSlashes,
    'dd-mm-yy':Date.DDMMYY.WithDashes,
    'yy':Date.YY,
    'yyyy':Date.YYYY,
    'month_num':Date.Month.Number,
    'month_abbr':Date.Month.Abbreviation,
    'date':Date.Day,
    'dow_number':Date.DayOfWeek.Number,
    'dow_abbr':Date.DayOfWeek.Abbreviation,
    'hh':Date.Time.HH,
    'min':Date.Time.MIN,
    'sec':Date.Time.SEC,
    'hhmin_23hr':Date.Time.HHMIN23hr,
    'hhmin_12hr':Date.Time.HHMIN12hr,
    'celsius':Format.Temperature.Celsius,
    'farenheit':Format.Temperature.Farenheit,
    'humidity':Format.Temperature.Humidity 
  } 
  


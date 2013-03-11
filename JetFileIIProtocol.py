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

class Animate:
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
  class Pause:
    @staticmethod
    def Seconds(seconds):
      #TODO: Better handling of seconds values greater than 99
      return '\x0e0{0:02d}'.format(seconds)

class Format:
  NewFrame = '\x0c'
  NewLine = '\x0d'
  Halfspace = '\x82'
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
    #text = (getattr(sys.modules['JetFileIIProtocol'],'Font')).n5x5 + text
    def ReplaceMarkupTags(match):
      code = match.group(1).strip()
      print "code is " + code
      if code in Markup.Registry:
          return Markup.Registry[code]
      return match.group(0)
    
    regex = re.compile(r"\{(.*?)\}")
    #text = re.sub(regex , '', text)
    text = re.sub(regex, ReplaceMarkupTags, text)
    print "subbed text: " + text
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

class Font:
  n5x5 = '\x1a0'
  n7x6 = '\x1a1'
  n14x8 = '\x1a2'
  n15x9 = '\x1a3'
  n16x9 = '\x1a4'
  n24x16 = '\x1a6'
  n11x9 = '\x1a:'
  n12x7 = '\x1a;'
  n22x18 = '\x1a<'
  n30x18 = '\x1a+'
  n40x21 = '\x1a>'
  b14x10 = '\x1aN'
  b15x10 = '\x1aO'
  b16x12 = '\x1aP'
  b24x8 = '\x1aQ'
  b32x8 ='\x1aR'
  b11x7 = '\x1aS'
  b12x7 = '\x1aT'
  b22x12 = '\x1aU'
  b40x21 = '\x1aV'
  class Color:
    Black = '\x1c\x30'
    Red = '\x1c\x31'
    Green = '\x1c\x32'
    Amber = '\x1c\x33'
    class Mixed:
      Characters = '\x1c\x34'
      Horizontal = '\x1c\x35'
      Wave = '\x1c\x36'
      Splash = '\x1c\x37'

#See section 3.1 of protocol description
class Message:
  class DisplayControlWithoutChecksum:
    Header = '\x00\x00\x00\x00\x00\x01Z00'
    Protocol = '\x06'
    BeginCommand = '\x02'
    WriteFile = 'A'
    Coda = '\x04'
    @staticmethod
    def Create(msgId, unit_address=0, disk='E', folder='T', text='Testing, 1, 2, 3.'):
      p = Message.DisplayControlWithoutChecksum
      f = Format
      m = Message
      return p.Header + p.BeginCommand + p.WriteFile + m.MsgId2DiskFolderFilename(msgId) + p.Protocol + f.InterpretMarkup(text) + p.Coda;
  @staticmethod
  def MsgId2Filename(msgId):
    #asciiMajor = 65 + int(msgId/26)
    #asciiMinor = 65 + int(msgId % 26)
    #return '{0:01c}{0:01c}'.format(asciiMajor,asciiMinor)
    return str('%c%c' % (65 + int(msgId / 26), 65 + (msgId % 26)))
  @staticmethod
  def MsgId2DiskFolderFilename(msgId,disk='E',folder='T'):
    return '\x0f' + disk + folder + Message.MsgId2Filename(msgId)
 
#There's gotta be a better way than this...
class Markup:
  Registry = {
    'Format.AutoTypeset.On' : Format.AutoTypeset.On,
    'Format.AutoTypeset.Off' : Format.AutoTypeset.Off,
    'Font.n5x5' : Font.n5x5,
    'Font.n7x6' : Font.n7x6,
    'Font.n12x7' : Font.n12x7,
    'Font.n16x9' : Font.n16x9,
    'Font.b22x12' : Font.b22x12,
    'Font.b32x8' : Font.b32x8
  } 
  


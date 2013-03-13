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
      arg = match.group(2).strip().lower()
      print "code: " + code +" arg: " + arg
      if code in Markup.Registry:
        #pass
        return Markup.Registry[code](arg)
      return match.group(0)
    def ReplaceMarkupTags(match):
      code = match.group(1).strip().lower()
      print "code is " + code
      if code in Markup.Registry:
          return Markup.Registry[code]
      return match.group(0)
    
    regex_with_arg = re.compile(r"\{(.*?)=(.*?)\}")
    regex = re.compile(r"\{(.*?)\}")
    text = re.sub(regex_with_arg, ReplaceMarkupTagWithArg, text)
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

#picture handling is described in protocol section 4
class Picture:
  @staticmethod
  def FromDiskFilename(filename,disk='E'):
    return '\x14'+disk+filename
  

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
  Header = '\x00\x00\x00\x00\x00\x01Z00'
  Protocol = '\x06'
  BeginCommand = '\x02'
  WriteFile = 'A'
  Coda = '\x04'
  class DisplayControlWithoutChecksum:
    @staticmethod
    def Create(msgId, unit_address=0, disk='E', folder='T', text='Testing, 1, 2, 3.'):
      p = Message.DisplayControlWithoutChecksum
      f = Format
      m = Message
      return m.Header + m.BeginCommand + m.WriteFile + m.MsgId2DiskFolderFilename(msgId) + m.Protocol + f.InterpretMarkup(text) + m.Coda
  @staticmethod
  def MsgId2Filename(msgId):
    #asciiMajor = 65 + int(msgId/26)
    #asciiMinor = 65 + int(msgId % 26)
    #return '{0:01c}{0:01c}'.format(asciiMajor,asciiMinor)
    return str('%c%c' % (65 + int(msgId / 26), 65 + (msgId % 26)))
  @staticmethod
  def MsgId2DiskFolderFilename(msgId,disk='E',folder='T'):
    return '\x0f' + disk + folder + Message.MsgId2Filename(msgId)

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
    'red' : Font.Color.Red,
    'green' : Font.Color.Green,
    'amber' : Font.Color.Amber,
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
    'peeloffright' : Animate.PeelOfRight.In,
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
    'peeloffright' : Animate.PeelOfRight.Out,
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
    '12x7' : Font.n12x7,
    '16x9' : Font.n16x9,
    'b22x12' : Font.b22x12,
    'b32x8' : Font.b32x8
  } 
  


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
  class Flash:
    Start = '\x071'
    Stop = '\x070'
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
  


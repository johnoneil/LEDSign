# vim: set ts=2 expandtab:
#******************************************************************************
#
# JetFileIIProtocol.py
# John O'Neil
# Saturday, March 9th 2012
#
# (simplified)JetfileII LED sign protocol derived off documentation
#
#******************************************************************************

class Flash:
  start = '\x071'
  stop = '\x070'

class Animate:
  class In:
    random = '\x0aI\x2f'
    jump = '\x0aI\x30'
    move_left = '\x0aI\x31'
    move_right = '\x0aI\x32'
    scroll_left = '\x0aI\x33'
    scroll_right = '\x0aI\x34'
  class Out:
    random = '\x0aO\x2f'
    jump = '\x0aO\x30'
    move_left = '\x0aO\x31'
    move_right = '\x0aO\x32'
    scroll_left = '\x0aO\x33'
    scroll_right = '\x0aO\x34'

NewFrame = '\x0c'
NewLine = '\x0d'

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
  


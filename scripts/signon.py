#!/usr/bin/env python

import serial
from JetFileII import Message

from config import PORT
from config import BAUD_RATE

def signon():
    msg = Message.TurnSignOn()

    ser = serial.Serial(PORT, BAUD_RATE)
    x = ser.write(msg)

    resp = ser.read()
    ser.flushInput()
    ser.flushOutput()

    ser.close()

if __name__ == '__main__':
    signon()

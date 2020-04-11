#!/usr/bin/env python

import serial
from serial import rs485
from JetFileII import Message

from config import PORT
from config import BAUD_RATE

def signoff():
    '''
    Turn LED sign off
    '''
    msg = Message.TurnSignOff(goodbyeMsg=False)

    ser = serial.Serial(PORT, BAUD_RATE)
    x = ser.write(msg)

    resp = ser.read()
    ser.flushInput()
    ser.flushOutput()

    ser.close()

if __name__ == '__main__':
    signoff()



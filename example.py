#!/usr/bin/env python3
"""Example script using acnet.py and Firmata"""

from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
from acnet import Device

ARDUINO = PyMata3()
REMOTE = Device('Z:REMOTE')
ARDUINO.read_pin = 2
ON = 1023
OFF = 0

ARDUINO.set_pin_mode(ARDUINO.read_pin, Constants.ANALOG)

def rawToVolts(raw):
    return raw/1023*5

while True:
    ARDUINO.sleep(1)
    readingVolts = rawToVolts(ARDUINO.analog_read(ARDUINO.read_pin))
    print(readingVolts)
    REMOTE.set_setting(readingVolts)
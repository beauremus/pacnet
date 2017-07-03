#!/usr/bin/env python
"""Interface to Arduino hardware"""

import time
import serial
from serial.tools import list_ports

class Arduino:
    """Object holding state for Arduino interface"""

    def __init__(self):
        """Sets the serial interface to Arduino USB device"""

        connected_devices = list_ports.comports()

        if connected_devices == []:
            raise IOError("Could not find an arduino - is it plugged in?")
        for pinfo in connected_devices:
            self.serial = serial.Serial(pinfo.device)

    def get_pin(self, pin_number):
        """Requests reading from Arduino using r character as prompt

        Args:
            pin_number (str): A two digit string representing the desired pin

        Returns:
            int: Raw voltage from Arduino
        """

        return arduino_request(self, 'r' + pin_number + '\n')

    def set_pin(self, pin_number, status):
        """Sets the desired pin to an 'on' (3.3V) state or an 'off' (0V) state

        Args:
            pin_number (str): A two digit string representing the desired pin
            status (str): A 0 or 1 boolean type value indicating desired pin status

        Returns:
            str: Sentence describing the action
        """

        return arduino_request(self, 'w' + pin_number + status + '\n')

def arduino_request(self, request):
    """Take a string request passed to Arduino

    Args:
        request (str): A string representing the request format
            bit 1 - 'w' for write or 'r' for read
            bit 2-3 - two digit representation of pin number
            bit 4 - boolean; 0 or 1 for Arduino bit status; only required for write

    Returns:
        float: Scaled reading of requested pin
    """

    format_request = request.encode('utf-8')
    self.serial.write(format_request)
    time.sleep(.05)
    arduino_response = self.serial.read(self.serial.inWaiting()).decode()
    third_response = arduino_response.split('\r')[2]
    if third_response == '':
        third_response = '0'
    return scale_reading(int(third_response))

def scale_reading(raw):
    """Scales the raw integer from Arduino to voltage

    Args:
        raw (int): An integer from Arduino to be scaled

    Returns:
        float: Scaled number for real voltage
    """

    return raw / 313.7

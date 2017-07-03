#!/usr/bin/env python
"""Example script using acnet.py and arduino.py"""

from arduino import Arduino
from acnet import Device

ARDUINO = Arduino()
BEAU = Device('G:BEAU')
REMOTE = Device('Z:REMOTE')
Q806_OUTPUT_PIN = '06'
Q806_PIN = '20'
V100_OUTPUT_PIN = '07'
V100_PIN = '21'

def compare_and_update(read_pin, device, write_pin):
    """Reads input pin and compares to device alarm min and max to determine output of output pin

        Args:
            read_pin (str): Two digit pin number
            device (obj): ACNET device object
            write_pin (str): Two digit pin number

        Returns:
            boolean: True if in tolerance
        """

    if in_tolerance(ARDUINO.get_pin(read_pin), device.get_alarm()):
        ARDUINO.set_pin(write_pin, '1')
        device.set_status(write_pin, '1')
        return 1
    else:
        ARDUINO.set_pin(write_pin, '0')
        device.set_status(write_pin, '0')
        return 0

def in_tolerance(value, tolerance):
    """Returns a boolean indicator of tolerance based on inputs

        Args:
            value (num): A value to compare to min and max
            tolerance (dict): Dictionary including min and max values

        Returns:
            boolean: True if within tolerance
    """

    if float(value) > tolerance['min'] and float(value) < tolerance['max']:
        return True
    else:
        return False

while True:
    compare_and_update(Q806_PIN, BEAU, Q806_OUTPUT_PIN)
    compare_and_update(V100_PIN, REMOTE, V100_OUTPUT_PIN)

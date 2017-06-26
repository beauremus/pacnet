#!/usr/bin/env python
"""This script runs forever writing the output of the Arduino to the designated Remote parameter."""

from xmlrpc.client import ServerProxy
import time
import serial
import serial.tools.list_ports as list_ports

SERIAL_NUMBER = '2631180'
status_store = 0
SERVER = ServerProxy('http://www-bd.fnal.gov/xmlrpc/Remote')

def find_arduino(serial_number):
    """Returns the serial interface to USB device based on input device number

    Args:
        serial_number (str): Serial number of attached Arduino

    Returns:
        The serial interface for communication with Arduino.

    """

    for pinfo in list_ports.comports():
        if pinfo.serial_number == serial_number:
            return serial.Serial(pinfo.device)
    raise IOError("Could not find an arduino - is it plugged in?")

ARDUINO_SERIAL = find_arduino(SERIAL_NUMBER)

def get_reading(pin_number):
    """Requests reading from Arduino using r character as prompt

    Args:
        pin_number (str): A two digit string representing the desired pin

    Returns:
        int: Raw voltage from Arduino

    """

    request = ('r' + pin_number + '\n').encode('utf-8')
    ARDUINO_SERIAL.write(request)
    time.sleep(.066)
    arduino_response = ARDUINO_SERIAL.read(ARDUINO_SERIAL.inWaiting()).decode()
    return int(arduino_response.split('\r')[0]) / 313.7

def send_setting(device, value):
    """Set the setting property of a given ACNET device
    """

    SERVER.Remote.setting(device, value)
    return 'Device, ' + device + ' has been set to a value of ' + str(value)

def set_setting(pin_number, status):
    """Sets the desired pin to an 'on' (3.3V) state or an 'off' (0V) state

    Args:
        pin_number (str): A two digit string representing the desired pin
        status (str): A 0 or 1 boolean type value indicating desired pin status

    Returns:
        str: Sentence describing the action

    """

    request = ('w' + pin_number + status + '\n').encode('utf-8')
    ARDUINO_SERIAL.write(request)
    return 'Pin number ' + pin_number + ' is now ' + status

def set_status(device, bit_number, status):
    """Sets a given bit in the digital status to the given status (0 or 1)

    Args:
        bit_number (str): Coresponds to ACNET digital status bit number
        status (boolean): Desired status value to be reflected in ACNET

    Returns:
        float: Global status_store; current status
    """

    global status_store

    is_on = status_store&(2**int(bit_number))

    if status and not is_on:
        toggle_status(device, bit_number)
    elif not status and is_on:
        toggle_status(device, bit_number)

    return status_store

def toggle_status(device, bit_number):
    """Toggles a given bit in the digital status

    Args:
        bit_number (int): Coresponds to ACNET digital status bit number

    Returns:
        float: Global status_store; current status
    """

    global status_store

    new_status = status_store^(2**int(bit_number))

    SERVER.Remote.status(device, float(new_status))

    status_store = new_status
    return status_store

"""Testcode
"""
while ARDUINO_SERIAL:
    set_setting('20', '1')
    read = get_reading('20')
    send_setting('G:BEAU', read)
    set_status('G:BEAU', '20', 1)


""" TODO: read alarm limits
    TODO: modularize code
"""

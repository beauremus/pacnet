#!/usr/bin/env python
"""Interface to the ACNET Remote OAC"""

from xmlrpc.client import ServerProxy
import re
import os

REMOTE = ServerProxy('http://www-bd.fnal.gov/xmlrpc/Remote').Remote
ALARM = ServerProxy('http://www-bd.fnal.gov/xmlrpc/Accelerator')

class Device:
    """Instantiates a connection to ACENT for a particular device
    ACNET device name must be a device already existing on Remote OAC
    """

    def __init__(self, device_name):
        self.name = device_name
        self.status = local_status(device_name)

    def set_setting(self, value):
        """Set the setting property of a given ACNET device

        Args:
            value (num): Any numerical value to be assigned to the device setting

        Returns:
            float: String representation of given value
        """

        REMOTE.Remote.setting(self.name, value)
        return float(value)

    def toggle_status_bit(self, bit_number):
        """Toggles a given bit in the digital status

        Args:
            device_name (str): ACNET device name; Must exist on Remote
            bit_number (int): Coresponds to ACNET digital status bit number

        Returns:
            float: Global status_store; current status

        """

        new_status = self.status^(2**int(bit_number))

        REMOTE.Remote.status(self.name, float(new_status))
        local_status(self.name, new_status)

        self.status = new_status
        return self.status

    def set_status(self, bit_number, status):
        """Sets a given bit in the digital status to the given status (0 or 1)

        Args:
            bit_number (str): Coresponds to ACNET digital status bit number
            status (boolean): Desired status value to be reflected in ACNET

        Returns:
            float: Global status_store; current status
        """

        is_on = self.status&(2**int(bit_number))

        if status and not is_on:
            self.toggle_status_bit(bit_number)
        elif not status and is_on:
            self.toggle_status_bit(bit_number)

        return self.status

    def get_alarm(self):
        """Returns a list with device properties
            See http://www-bd.fnal.gov/xmlrpc/Accelerator for details

            Return:
                list: min and max values of alarm
        """

        data = ALARM.getReading(self.name.replace(':', '@'))

        return {'max': data['maxscaled'], 'min': data['minscaled']}

def local_status(device_name, value=None):
    """Interface to get and set local_status

        Args:
            device_name (str): String representing ACNET device name
            value (str): String representing binary status value of given device

        Returns:
            str: String representing current binary status
    """

    if value is None:
        status = get_local_status(device_name)
    else:
        status = set_local_status(device_name, value)

    return status

def get_local_status(device_name):
    """Gets the status of a given device in a local text file

        Args:
            device_name (str): String representing ACNET device name

        Returns:
            str: String representing current binary status
    """

    if not os.path.isfile('status.acnet'):
        return set_local_status(device_name, '0')
    else:
        regex = re.compile(device_name + r'\t\d+\n')
        with open('status.acnet', 'r') as file:
            lines = file.read()
            value = regex.findall(lines)
            status = value[0].rstrip().split()[1]
        return status

def set_local_status(device_name, value):
    """Sets the status of a given device in a local text file

        Args:
            device_name (str): String representing ACNET device name
            value (str): String representing binary status value of given device

        Returns:
            str: String representing current binary status
    """

    mode = 'r+'
    if not os.path.isfile('status.acnet'):
        mode = 'w+'
    regex = re.compile(device_name + r'\t\d+\n')
    with open('status.acnet', mode) as file:
        lines = file.read()
        if lines == '':
            file.write(device_name + '\t' + value + '\n')
        else:
            lines = regex.sub(device_name + '\t' + value + '\n', lines)
            file.seek(0)
            file.write(lines)
    return value

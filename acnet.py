#!/usr/bin/env python
"""Interface to the ACNET Remote OAC"""

from xmlrpc.client import ServerProxy

REMOTE = ServerProxy('http://www-bd.fnal.gov/xmlrpc/Remote')
ALARM = ServerProxy('http://www-bd.fnal.gov/xmlrpc/Accelerator')

class Device:
    """Instantiates a connection to ACENT for a particular device
    ACNET device name must be a device already existing on Remote OAC
    """

    def __init__(self, device_name):
        self.name = device_name
        self.status = '0'

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

        self.status = new_status
        return self.status

    def set_status_bit(self, bit_number, status):
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

    def set_status(self, status):
        """Sets the digital status to the related device

        Args:
            status (boolean): Desired status value to be reflected in ACNET

        Returns:
            float: Global status_store; current status
        """

        REMOTE.Remote.status(self.name, float(status))

        self.status = status
        return self.status

    def get_status(self):
        """Gets the digital status to the related device

        Returns:
            float: Global status_store; current status
        """

        return self.status

    def get_alarm(self):
        """Returns a list with device properties
            See http://www-bd.fnal.gov/xmlrpc/Accelerator for details

            Return:
                list: min and max values of alarm
        """

        data = ALARM.getReading(self.name.replace(':', '@'))
        if 'maxscaled' not in data or 'minscaled' not in data:
            return {'max': None, 'min': None}

        return {'max': data['maxscaled'], 'min': data['minscaled']}

#!/usr/bin/python

import serial.tools.list_ports as list_ports

ports = list(list_ports.comports())

for p in ports:
    print(p.serial_number)

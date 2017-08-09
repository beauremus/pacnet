# Pi-ACNET Interface (PACNET)

## Getting Started

Getting started will walk you through setup that is required before using the Pi-ACNET interface.

## Equipment

It may be possible to use sensor hardware directly with the Raspberry Pi, without a microcontroller, but this implemenation uses Arduino to modularize the interface for ease of use with many different sensors.

  - Arduino
    - USB cable with correct terminations
  - Raspberry Pi
    - SD Card with at least 8GB of capacity, faster = better

## Installation

Choose the appropriate `.ino` file for your use from the `arduino` folder and upload that file to the Arudino.
Refer to the [Arduino website](https://www.arduino.cc/en/Guide/HomePage) for more detailed information on uploading code to the board.

Install [Raspbian-lite](https://www.raspberrypi.org/downloads/raspbian/) on an SD card and then use the SD card to boot the Raspberry Pi.

Download this repository into the pi user home folder.

### Startup

Ideally the PACNET package runs headless without any necessary intervention to function in the field.

In order to have the `write.py` run on startup, add the launch command to the `/etc/rc.local` file.

I have found this method unreliable and am looking for a systemd solution.

## ACNET Configuration

Permissions are needed to create a new ACNET device. Brian Hendricks is the contact for these permissions.

From the D80 application, start by entering and returning Z:REMOTE into the device name field. In the top right corner use the Pgm_Tools menu to Enable Edit. Now type the desired name of your new device over Z:REMOTE in the name field. You will be presented with a menu. Choose Create a new device.

Modify your new device description and add or remove any properties that you need for you device.

## XML-RPC

Once your target device exists you can use any language with an XML-RPC library to send a setting value to the target device via [Remote http://www-bd.fnal.gov/xmlrpc/Remote](http://www-bd.fnal.gov/xmlrpc/Remote). See the `acnet.py` example.

It is possible to structure the request without a library. Refer to the [spec](http://xmlrpc.scripting.com/spec.html) for more information.

## TODO

 - Auto-install systemd
 
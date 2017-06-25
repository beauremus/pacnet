# Python-ACNET Interface (PACNET)

## Getting Started

Getting started will walk you through setup that is required before using the Python-ACNET interface.

## Equipment

  - Arduino
  - Raspberry Pi

## Installation

Choose the appropriate `.ino` file for your use from the `arduino` folder and upload that file to the Arudino.
Refer to the [Arduino website](https://www.arduino.cc/en/Guide/HomePage) for more detailed information on uploading code to the board.

Install [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) on an SD card and then use the SD card to boot the Raspberry Pi.

Download this repository into the pi home folder.

### Arduino Association

After plugging in the Arduino via USB run `python3 arduinoSN.py`. This will print the serial number of the Arduino. Copy the serial number and open `write.py` in your favorite editor. Replace the value assigned to `SERIAL_NUMBER` with the serial number you copied from `arduinoSN.py`.

If you change the Arduino board you will need repeat the above procedure to associate the new board with the Raspberry Pi.

### Startup

Ideally PACNET package runs headless without any necessary intervention to function in the field.

In order to have the `write.py` run on startup, add `./pacnet/autoStart.sh` to the `.bashrc` file in the pi home directory.

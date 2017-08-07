# Pi-ACNET Interface (PACNET)

## Getting Started

Getting started will walk you through setup that is required before using the Python-ACNET interface.

## Equipment

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

In order to have the `write.py` run on startup, add `./pacnet/autoStart.sh` to the `.bashrc` file in the pi home directory.

## TODOs

  - Pull down resistors
  - Constant current transistor
  - Differential OpAmp for inputs
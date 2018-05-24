# Pi-ACNET Interface (PACNET)

The repository name was chosen for the original implemenation of this code, requiring a Raspberry Pi. I have since generalized the code.

## Arduino protocol installation

Using the Arduino IDE select `File>Examples>Firmata>StandardFirmataPlus` and compile/upload to the chosen board.
Refer to the [Arduino website](https://www.arduino.cc/en/Guide/HomePage) for more detailed information on uploading code to the board.
Refer to the [Firmata protocol](https://github.com/firmata/arduino) for more detailed information on uploading code to the board.

## Firmata usage

[Firmata for Arduino](https://github.com/firmata/arduino) supports many languages with libraries to easily communicate with your board.

I have implemented a [simple example](example.py) using the [pymata library](https://github.com/MrYsLab/pymata-aio) for Python. Be aware that this example is basic and the documentation suggests using a [callback structure](https://gist.github.com/MrYsLab/0b9f125f04f171065af0) to get data.

This code is run from the computer attached to the Arduino board via USB whether it be a laptop or Raspberry Pi.
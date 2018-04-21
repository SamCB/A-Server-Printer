# A Server Printer

Code for the [Raspberry Pi](https://www.raspberrypi.org/) and the [Adafruit Mini Thermal Receipt Printer](https://www.adafruit.com/product/597) to connect to my [A Server](https://github.com/SamCB/A-Server) project, and print out whatever is on it.

Written in Python, for Python 3.
Makes use of a slightly modified version of [Adafruit's provided Python Library](https://github.com/adafruit/Python-Thermal-Printer/blob/master/Adafruit_Thermal.py). See `Adafruit_Thermal.py` for licensing (hint: MIT) and more info.

Currently a work in progress.

## Getting Started

### Hardware Dependencies

* Rasbperry Pi installed with Raspbian and internet/wifi connection
* [Adafruit Mini Thermal Receipt Printer](https://www.adafruit.com/product/597)
* 1x LED
* 2x Momentary Push Switches

### Software Dependencies

To run as I wrote it (for retrieving from [A Server](https://github.com/SamCB/A-Server)) you will need 

* Python 3
* RPi.GPIO
* [Python Requests](http://docs.python-requests.org/en/master/)
* An instance of [A Server](https://github.com/SamCB/A-Server) running up on AWS lambda

And optionally:

* [Emoji2Text](https://github.com/SamCB/Emoji2Text) - A library I wrote to replace emoji with their text based version. Without it, will just print a few question marks when you come to emoji.

Of course, it should be pretty easy to repurpose the software to communicate with something else.
Just re-implement the `AServerConnection` object in `communications` to connect to whatever endpoint you want using whatever library you want.

### Hardware Setup

* Printer Input to Pi Tx
* Printer Ground to Pi Ground
* Printer Output disconnected (I wasn't able to get this working, if connected, needs a resistor)
* "Print" button to pin 23 (BCM)
* "Clear Server" button to pin 24 (BCM)
* LED to pin 25 (BCM)

### Software Setup

Copy `.config.example.json` to `.config.json`.
Change variables to your local setup.
You can add any extra config defined in `DEFAULT_CONFIG` of `main.py`.

## Troubleshooting

* *The printer prints without being told to:*

    Run the config:

        sudo raspi-config

    Go to `5 Interfacing Options` -> `P6 Serial`.
    Disable login shell over serial but keep serial port hardware enabled.
    It should display a message:

        The serial login shell is disabled
        The serial interface is enabled

    Then edit the file `/boot/cmdline.txt`

        sudo nano /boot/cmdline.txt

    And remove any `console=serial0,xxxxxx` style setting.
    Do not remove `console=tty1`.

    Restart the Raspberry Pi.

    Printing should now behave as expected.

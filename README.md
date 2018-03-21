# A Server Printer

Code for the [Raspberry Pi](https://www.raspberrypi.org/) and the [Adafruit Mini Thermal Receipt Printer](https://www.adafruit.com/product/597) to connect to my [A Server](https://github.com/SamCB/A-Server) project, and print out whatever is on it.

Written in Python, for Python 3.
Makes use of a slightly modified version of [Adafruit's provided Python Library](https://github.com/adafruit/Python-Thermal-Printer/blob/master/Adafruit_Thermal.py). See `Adafruit_Thermal.py` for licensing (hint: MIT) and more info.

Currently a work in progress.

## Getting Started

### Software Dependencies

* Python 3
* RPi.GPIO
* Python Requests

### Setup

Copy `.config.example.json` to `.config.json`.
Change variables to your local setup.
You can add any extra config defined in `DEFAULT_CONFIG` of `main.py`.

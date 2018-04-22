# A Server Printer

Code for the [Raspberry Pi](https://www.raspberrypi.org/) and the [Adafruit Mini Thermal Receipt Printer](https://www.adafruit.com/product/597) to connect to my [A Server](https://github.com/SamCB/A-Server) project, and print out whatever is on it.

Written in Python, for Python 3.
Makes use of a slightly modified version of [Adafruit's provided Python Library](https://github.com/adafruit/Python-Thermal-Printer/blob/master/Adafruit_Thermal.py). See `Adafruit_Thermal.py` for licensing (hint: MIT) and more info.

## Getting Started

### Hardware Dependencies

* Rasbperry Pi installed with Raspbian and internet/wifi connection (I use a Pi Zero W)
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
* "Print" button to Pi pin 23 (BCM) and ground
* "Clear Server" button to Pi pin 24 (BCM) and ground
* LED + to Pi pin 25 (BCM) and - to ground

Pins for the buttons and LED can be changed in `.config.json` (see Software Setup).

### Software Setup

Copy `.config.example.json` to `.config.json`.
Change variables to your local setup.
You can add any extra config defined in `DEFAULT_CONFIG` of `main.py`.

You'll then need to set the app to run whenever the pi turns online.
I've provided a short script to help you with this. Call:

    sudo ./setup-runtime

It'll create a new script in `/etc/init.d/` and subscribes it to startup.

After this point, if you restart the pi:

    sudo reboot

Wait a bit, and then you should see the status led flashing.
Once it gives three long pulses and switches off, it's ready to print.

## Runtime

Press the "print" button (default pin 23) to connect to the server and print.
Press the "clear server" button (default pin 24) to wipe whatever is on the server.
The button on the thermal printer feeds the paper a few extra rows.

Text being printed is formatted accordingly:

* attempted conversion of emoji to a text representation (e.g. 😎 to `[smiling face with sunglasses]`);
* safe conversion of a few common unicode replacements (e.g. quotation marks);
* removal of other unicode; and 
* wrapping text to fit within the 32 character spacing

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

* *Things aren't starting up and I don't know what's going wrong!*

    Take a look at the logs in `~/log/printer.log`. That might help.

* *Emoji aren't printing as text even though I installed emoji2text*

    Because of how startup scripts are called, python is running under sudo.
    So a workaround that I've found is to install emoji2text using `sudo pip`...

        sudo pip3 install emoji2text

    I'm not 100% happy with this solution, but I have been running out time so
    this is the quickest workaround I've got...


## Future Work

I'm not sure I'm going to do much more on this.
As with any project, there are a heap of things I'd have done differently if I had my time again.
I've actually been tossing up about rebuilding it some time with something like an ESP8266 instead of a pi, which would of course mean this entire library needs to be thrown out.
That said, if anyone has suggestions or contributions, please let me know.
If you've used any of what I've written for some of your own work, I'd love to hear about them.

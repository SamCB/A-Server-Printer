import RPi.GPIO as GPIO
import json
import time
from os import path

from app.printer_logging import get_logger
from app.app import App

logger = get_logger(__name__)

DEFAULT_CONFIG = {
    # ======= GPIO Config =======
    'GPIO_MODE': GPIO.BCM,
    # Print Button Pin number
    'BUTTON_A': 23,
    # Clear Server Pin number
    'BUTTON_B': 24,
    # Pin number for LED
    'LED': 25,
    # If > 0, will run that pin as HIGH output while the program is running
    # I use this to selectively provide power to the printer via a MOSFET.
    'PRINTER_POWER': -1,

    # ======= Printer Config =======
    # Connection arguments passed to the Adafruit_Thermal object which itself
    # is an extension of the serial.Serial object:
    # https://pyserial.readthedocs.io/en/latest/pyserial.html
    'PRINTER_CONNECTION': {
        'port': '/dev/serial0',
        'baudrate': 19200,
        'timeout': 3
    },

    # ======= Server Config =======
    # Connection details to the "A-Server":
    # https://github.com/SamCB/A-Server
    'SERVER': 'localhost:3000',
    'PASSWORD': 'SECRET',
}

CONFIG = path.join(path.dirname(path.abspath(__file__)), '.config.json')

if __name__ == "__main__":
    try:
        logger.info("Loading Config from: %s", CONFIG)
        with open(CONFIG) as f:
            config = {**DEFAULT_CONFIG, **json.load(f)}
    except FileNotFoundError:
        logger.fatal('No config file found. Read through README for instructions on how to get started.')
    else:
        logger.info("Config Loaded Startup App")
        app = App(config)
        logger.info("App Running")
        try:
            while True:
                time.sleep(120)
        except KeyboardInterrupt:
            pass
        finally:
            app.teardown()
            print()

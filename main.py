import RPi.GPIO as GPIO
import json
import time
from os import path

from app.printer_logging import get_logger
from app.app import App

logger = get_logger(__name__)

DEFAULT_CONFIG = {
    'GPIO_MODE': GPIO.BCM,
    'BUTTON_A': 23,
    'BUTTON_B': 24,
    'LED': 25,
    'PRINTER_CONNECTION': {
        'port': '/dev/serial0',
        'baudrate': 19200,
        'timeout': 3
    },
    'SERVER': 'localhost:3000',
    'PASSWORD': 'SECRET'
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

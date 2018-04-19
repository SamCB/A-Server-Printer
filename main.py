import RPi.GPIO as GPIO
import json
import time
import logging

from app import App

logger = logging.getLogger(__name__)

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

if __name__ == "__main__":
    try:
        logger.info("Loading Config")
        with open('.config.json') as f:
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

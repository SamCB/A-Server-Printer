import RPi.GPIO as GPIO

from led import LED
from button import Button
from printer import Printer

DEFAULT_CONFIG = {
    'GPIO_MODE': GPIO.BCM,
    'BUTTON_A': 22,
    'BUTTON_B': 23,
    'LED_A': 18,
    'LED_B': 17,
    'PRINTER_CONNECTION': {
        'port': '/dev/serial0',
        'baudrate': 19200,
        'timeout': 3
    }
}


def setup(config):
    GPIO.setmode(config['GPIO_MODE'])

    # LED Setup
    ledA = LED(config['LED_A'])
    ledB = LED(config['LED_B'])

    # Printer Setup
    p = config['PRINTER_CONNECTION']
    printer = Printer(p['port'], p['baudrate'], timeout=p['timeout'])

    # Button Setup
    buttonA = Button(config['BUTTON_A'])
    buttonB = Button(config['BUTTON_B'])

    buttonA.subscribe(lambda _: ledA.flash(1))
    buttonB.subscribe(lambda _: ledB.flash(1))


    return {
        'ledA': ledA, 'ledB': ledB,
        'buttonA': buttonA, 'buttonB': buttonB,
        'printer': printer
    }

def teardown():
    GPIO.cleanup()

if __name__ == "__main__":
    setup(DEFAULT_CONFIG)
    try:
        input("Any Key to Exit")
    except KeyboardInterrupt:
        pass
    finally:
        teardown()
        print()

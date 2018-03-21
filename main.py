import RPi.GPIO as GPIO
import json

from led import LED
from button import Button
from printer import Printer
from communications import AServerConnection

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
    },
    'SERVER': 'localhost:3000',
    'PASSWORD': 'SECRET'
}


def setup(config):
    GPIO.setmode(config['GPIO_MODE'])

    # LED Setup
    ledA = LED(config['LED_A'])
    ledB = LED(config['LED_B'])

    # Printer Setup
    p = config['PRINTER_CONNECTION']
    printer = Printer(p['port'], p['baudrate'], timeout=p['timeout'])
    printer.feed(1)

    # Server Connection
    conn = AServerConnection(config['SERVER'], config['PASSWORD'])

    def print_from_server(*_, **__):
        print("Printing")
        response = conn.read()
        print(response)
        printer.println(response)
        printer.feed(3)

    def clear_server(*_, **__):
        print("CLEARING")
        conn.write('')
        print("Cleared")

    # Button Setup
    buttonA = Button(config['BUTTON_A'])
    buttonB = Button(config['BUTTON_B'])

    buttonA.subscribe(lambda _: ledA.flash(1))
    buttonA.subscribe(print_from_server)

    buttonB.subscribe(lambda _: ledB.flash(1))
    buttonB.subscribe(lambda c: printer.println('c: {}'.format(c)))


    return {
        'ledA': ledA, 'ledB': ledB,
        'buttonA': buttonA, 'buttonB': buttonB,
        'printer': printer, 'conn': conn
    }

def teardown():
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        with open('.config.json') as f:
            config = {**DEFAULT_CONFIG, **json.load(f)}
    except FileNotFoundError:
        print('No config file found. Read through README for instructions on how to get started.')
    else:
        try:
            val = setup(config)
            val['printer'].format_print("""
# Hello World!

I really hope *that* you like_what_ is coming out of this printer. It should be
really ~fantastic~!

🔥🔥🔥
""")
            input("Any Key to Exit")
        except KeyboardInterrupt:
            pass
        finally:
            teardown()
            print()

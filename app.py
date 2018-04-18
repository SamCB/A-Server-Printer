import RPi.GPIO as GPIO

import threading

from led import LED
from button import Button
from printer import Printer
from communications import AServerConnection

class App:

    @classmethod
    def start_threaded(cls, endpoints):
        thread = threading.Thread(target=cls, args=(endpoints, ))
        return thread

    LED_SIGNALS = {
        'STARTUP': (0.1, '- - '),
        'READY': (0.75, '-- -- -- '),
        'CONNECTING': (0.1, '- -   - -   *'),
        'PRINTING': (0.5, '- - - *')
    }

    def __init__(self, config):
        self._bootstrap(config)
        self.led_signal('READY')

    def _bootstrap(self, config):
        GPIO.setmode(config['GPIO_MODE'])

        # LED Setup
        self.led = LED(config['LED'])
        finished = self.continous_led_signal('STARTUP')

        # Button Setup
        self.buttonA = Button(config['BUTTON_A'])
        self.buttonB = Button(config['BUTTON_B'])

        self.buttonA.subscribe(self.print_from_server)
        self.buttonB.subscribe(self.clear_server)

        # Printer Setup
        printer_config = config['PRINTER_CONNECTION']
        self.printer = Printer(
            printer_config['port'], printer_config['baudrate'],
            timeout=printer_config['timeout']
        )

        # Server Connection
        self.conn = AServerConnection(config['SERVER'], config['PASSWORD'])

        finished()

    def print_from_server(self, *_, **__):
        finished = self.continous_led_signal('CONNECTING')
        response = self.conn.futures_read()

        def print_response(r):
            finished()
            self.printer.batch_print(r.result())

        response.add_done_callback(print_response)

    def _wait_print_server(self, pin, time_held):
        if time_held > 3:
            self.clear_server()

    def clear_server(self, *_, **__):
        finished = self.continous_led_signal('CONNECTING')
        response = self.conn.futures_write('')
        response.add_done_callback(lambda *_, **__: finished())

    def led_signal(self, signal):
        return self.led.pattern(*self.LED_SIGNALS[signal])

    def continous_led_signal(self, signal):
        return self.led.repeated_pattern(*self.LED_SIGNALS[signal])

import RPi.GPIO as GPIO

from .printer_logging import get_logger

class App:

    LED_SIGNALS = {
        'STARTUP': (0.1, '- - '),
        'READY': (0.75, '-- -- -- '),
        'CONNECTING': (0.1, '- -   - -   *'),
        'PRINTING': (0.5, '- - - *')
    }

    def __init__(self, config):
        self.logger = get_logger(__name__)
        self.logger.info("Start Bootstrap")
        self._bootstrap(config)

        self.led_signal('READY')
        self.logger.info("Ready for print")

    def _bootstrap(self, config):
        self.logger.debug("Setup GPIO")
        # I'm running the imports inside this function so the LED can start
        #  blinking sooner so I know something is happening
        GPIO.setmode(config['GPIO_MODE'])

        # LED Setup
        self.logger.debug("Setup LEDs")
        from .led import LED
        self.led = LED(config['LED'])
        self.logger.debug("LEDs Setup - Start Signalling")

        finished = self.continous_led_signal('STARTUP')

        # Button Setup
        self.logger.debug("Setup Buttons")
        from .button import Button
        self.buttonA = Button(config['BUTTON_A'])
        self.buttonB = Button(config['BUTTON_B'])

        self.logger.debug("Buttons online setup subscriptions")
        self.buttonA.subscribe(self.print_from_server)
        self.buttonB.subscribe(self.clear_server)

        # Printer Setup
        self.logger.debug("Setup printer")
        from .printer import Printer
        if config['PRINTER_POWER'] > 0:
            GPIO.setup(config['PRINTER_POWER'], GPIO.OUTPUT)
            GPIO.output(config['PRINTER_POWER'], GPIO.HIGH)

        printer_config = config['PRINTER_CONNECTION']
        self.printer = Printer(
            printer_config['port'], printer_config['baudrate'],
            timeout=printer_config['timeout']
        )

        # Server Connection
        self.logger.debug("Setup Server Connection")
        from .communications import AServerConnection
        self.conn = AServerConnection(config['SERVER'], config['PASSWORD'])

        self.logger.debug("Bootstreap complete")
        finished()

    def print_from_server(self, *_, **__):
        self.logger.info("Print message")
        self.logger.debug("Connect to server")
        finished = self.continous_led_signal('CONNECTING')
        response = self.conn.futures_read()

        def print_response(r):
            finished()
            msg = r.result()
            self.logger.debug("Message received... printing {} bytes".format(len(msg)))
            self.printer.batch_print(r.result())

        response.add_done_callback(print_response)

    def clear_server(self, *_, **__):
        self.logger.info("Clear Server")
        finished = self.continous_led_signal('CONNECTING')
        response = self.conn.futures_write('')
        response.add_done_callback(lambda *_, **__: finished())
        response.add_done_callback(lambda *_, **__: self.logger.debug("Server Cleared"))

    def led_signal(self, signal):
        return self.led.pattern(*self.LED_SIGNALS[signal])

    def continous_led_signal(self, signal):
        return self.led.repeated_pattern(*self.LED_SIGNALS[signal])

    def teardown(self):
        self.logger.info("Shutting Down")
        GPIO.cleanup()
        self.printer.cleanup()
        self.conn.cleanup()
        self.logger.debug("Teardown complete")

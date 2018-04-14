import threading

class App:

    @classmethod
    def start_threaded(cls, endpoints):
        thread = threading.Thread(target=cls, args=(endpoints, ))
        return thread

    LED_SIGNALS = {
        'STARTUP': (1, '- - '),
        'READY': (0.75, '-- -- -- ')
    }

    def __init__(self, endpoints):
        self.led = endpoints['led']
        self.buttonA = endpoints['buttonA']
        self.buttonB = endpoints['buttonB']
        self.printer = endpoints['printer']
        self.conn = endpoints['conn']

    def _startup(self, config):
        startup_kill = self.continous_led_signal('STARTUP')

        startup_kill()
        self.led_signal('READY')

    def print_from_server(self, *_, **__):
        response = self.conn.futures_read()

        response.add_done_callback(
            lambda r: self.printer.batch_print(r.result())
        )

    def clear_server(self, *_, **__):
        self.conn.write('')

    def led_signal(self, signal):
        self.led.pattern(*self.LED_SIGNALS[signal])

    def continous_led_signal(self, signal):
        return self.led.repeated_pattern(*self.LED_SIGNALS[signal])

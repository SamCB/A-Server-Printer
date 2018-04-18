import RPi.GPIO as GPIO

import time

class Button:

    def __init__(self, pin):
        self.pin = pin

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.RISING, bouncetime=200)

        self.call_times = []

    def subscribe(self, callback):
        self.call_times.append(time.time())

        GPIO.add_event_callback(
            self.pin, lambda _: self._callback(callback)
        )

    def _callback(self, callback):
        def wait_range(n, t):
            for i in range(n):
                yield i
                time.sleep(t)

        callback([GPIO.input(self.pin) for _ in wait_range(1000, 0.02)])

    def clear_subscriptions(self):
        GPIO.remove_event_detect(self.pin)


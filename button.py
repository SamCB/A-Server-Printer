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
        start = time.time()
        GPIO.wait_for_edge(self.pin, GPIO.FALLING, timeout=3000)
        diff = time.time() - start
        callback(self.pin, diff)

    def clear_subscriptions(self):
        GPIO.remove_event_detect(self.pin)


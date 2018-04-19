import RPi.GPIO as GPIO

import time

class Button:

    def __init__(self, pin):
        self.pin = pin

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.RISING, bouncetime=200)

        self.last_pressed = time.time()

    def subscribe(self, callback):
        GPIO.add_event_callback(
            self.pin, lambda _: self._callback(callback)
        )

    def _callback(self, callback):
        # Super rough, kinda bad deduping because the bouncetime argument
        #  doesn't seem to do enough
        if time.time() - self.last_pressed > 1:
            self.last_pressed = time.time()
            callback()

    def clear_subscriptions(self):
        GPIO.remove_event_detect(self.pin)


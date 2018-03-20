import RPi.GPIO as GPIO
import time

class Button:

    def __init__(self, pin):
        self.pin = pin

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.RISING, bouncetime=200)

        self.call_times = []

    def subscribe(self, callback):
        index = len(self.call_times)
        self.call_times.append(time.time())

        GPIO.add_event_callback(
            self.pin, lambda c: self._manual_debounce(index, lambda: callback(c))
        )

    def _manual_debounce(self, index, callback, diff=0.2):
        # Manual debounce checks the last time we had this particular callback
        #  and if it was too recent, we ignore it
        # For some reason the bouncetime argument to add_event_detect doesn't
        #  seem to help too much
        now = time.time()
        if now - diff > self.call_times[index]:
            self.call_times[index] = now
            callback()

    def clear_subscriptions(self):
        GPIO.remove_event_detect(self.pin)

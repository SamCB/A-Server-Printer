import RPi.GPIO as GPIO

import threading
import time

class LED:

    def __init__(self, pin):
        self.pin = pin

        GPIO.setup(self.pin, GPIO.OUT)
        self.off()

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def flash(self, wait):
        # Use threading so we don't block other actions
        def t():
            self.on()
            time.sleep(wait)
            self.off()

        thread = threading.Thread(target=t)
        thread.start()

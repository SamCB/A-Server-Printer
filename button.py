import RPi.GPIO as GPIO

class Button:

    def __init__(self, pin):
        self.pin = pin

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.RISING)

    def subscribe(self, callback):
        GPIO.add_event_callback(self.pin, callback)

    def clear_subscriptions(self):
        GPIO.remove_event_detect(self.pin)

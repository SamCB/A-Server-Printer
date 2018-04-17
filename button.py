import RPi.GPIO as GPIO

import time
import threading

class Button:

    def __init__(self, pin):
        self.pin = pin

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.thread = _Button_Thread(self.pin)
        self.thread.start()

    def subscribe(self, callback):
        index = len(self.call_times)
        self.call_times.append(time.time())

        GPIO.add_event_callback(
            self.pin, lambda c: self._manual_debounce(index, lambda: callback(c))
        )

    def clear_subscriptions(self):
        GPIO.remove_event_detect(self.pin)

class _Button_Thread(threading.Thread):
    """
    Important Note! Button Thread assumes someone is going to do the cleanup for it!
    """
    def __init__(self, pin):
        super().__init__()
        self.daemon = True

        self.pin = pin

        self.callback_lock = threading.Lock()
        self.callbacks = []

    def add_callback(self, callback):
        with self.callback_lock:
            self.callbacks.append(callback)

    def clear_callbacks(self):
        with self.callback_lock:
            self.callbacks = []

    def run(self):
        while True:
            try:
                GPIO.wait_for_edge(self.pin, GPIO.FALLING)
            except RuntimeError as e:
                print("Error", e, "for pin", self.pin)
                continue

            start = time.time()
            GPIO.wait_for_edge(self.pin, GPIO.RISING)
            diff = time.time() - start
            with self.callback_lock:
                for callback in self.callbacks:
                    callback(self.pin, diff)


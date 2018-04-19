import RPi.GPIO as GPIO

from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import time

class Button:

    def __init__(self, pin):
        self.pin = pin

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.RISING, bouncetime=200)

        self.running = False
        self.executor_lock = Lock()
        self.executor = ThreadPoolExecutor()

    def subscribe(self, callback):
        GPIO.add_event_callback(
            self.pin, callback
        )

    def subscribe_held(self, callback, max_time):
        GPIO.add_event_callback(
            self.pin, lambda _: self._start_tracking(max_time, callback)
        )

    def _start_tracking(self, max_time, callback):
        print("START")
        with self.executor_lock:
            print("RUNNING?", self.running)
            if self.running:
                print("ALREADY RUNNING")
                return
            self.running = True

        print(self.running)
        print("SUBMIT")
        future = self.executor.submit(self._track_button, max_time)
        future.add_done_callback(lambda f: callback(f.result()))
        future.add_done_callback(self._finished_tracking)

    def _finished_tracking(self, *_):
        print("FINISHED")
        self.running = False

    def _track_button(self, max_time):
        def wait_range(n, t):
            for i in range(n):
                yield i
                time.sleep(t/n)

        now = time.time()
        debounce_count = 0
        for _ in wait_range(max_time, 0.2):
            val = GPIO.input(self.pin)
            print("VAL: ", val)
            if val == 1:
                if debounce_count == 5:
                    break
                debounce_count += 1
            else:
                debounce_count = 0

        return time.time() - now

    def clear_subscriptions(self):
        GPIO.remove_event_detect(self.pin)


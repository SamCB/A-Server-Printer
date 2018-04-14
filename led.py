import RPi.GPIO as GPIO

import threading
import time

class LED:

    ON = '-'
    OFF = ' '

    def __init__(self, pin):
        self.pin = pin

        GPIO.setup(self.pin, GPIO.OUT)
        self.off()

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def flash(self, wait):
        self.pattern(wait, '-')

    def pattern(self, rate, pattern):
        # Use threading so we don't block other actions
        def t():
            for p in pattern:
                if p == self.ON:
                    self.on()
                elif p == self.OFF:
                    self.off()
                else:
                    continue

                time.sleep(rate)
            self.off()

        thread = threading.Thread(target=t)
        thread.start()

    def repeated_pattern(self, rate, pattern):
        def t(lock, kill):
            i = 0
            while True:
                with lock:
                    if kill.is_set():
                        break

                    p = pattern[i % len(pattern)]
                    i += 1

                    if p == self.ON:
                        self.on()
                    elif p == self.OFF:
                        self.off()
                    else:
                        continue

                time.sleep(rate)

            self.off()

        def quieten(lock, kill):
            # Quickly turn off the LED in case we're stuck asleep
            while True:
                with lock:
                    if kill.is_set():
                        self.off()
                        break
                time.sleep(0.2)

        lock = threading.Lock()
        kill = threading.Event()

        thread_light = threading.Thread(target=t, args=(lock, kill))
        thread_quieten = threading.Thread(target=quieten, args=(lock, kill))
        thread_light.start()
        thread_quieten.start()

        # Return a trigger to kill pattern calling
        return kill.set


import RPi.GPIO as GPIO

import threading

class LED:

    ON = '-'
    OFF = ' '
    REPEAT = '*'

    KILL_THREAD = 'KILL_THREAD'

    def __init__(self, pin):
        self.pin = pin

        GPIO.setup(self.pin, GPIO.OUT)
        self._off()

        self.thread_management_lock = threading.Lock()
        self.thread = None

    def _on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def _off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def flash(self, wait):
        """
        Turn on the LED for the given period of time in seconds

        Return an interrupt function for turning the LED off.
        """
        return self.pattern(wait, '-')

    def pattern(self, rate, pattern):
        """
        Flash the LED in a given pattern at the given rate.

        Return an interrupt function for cancelling the pattern and turning the
        LED off
        """
        with self.thread_management_lock:
            if self.thread is not None:
                self.thread.kill()

            self.thread = _LED_Thread(pattern, rate, self._on, self._off)
            self.thread.start()

        return self.thread.kill

    def repeated_pattern(self, rate, pattern):
        """
        Flash the LED in a given pattern at the given rate, on repeat.

        Return an interrupt function for cancelling the pattern and turning the
        LED off
        """
        return self.pattern(rate, '{}{}'.format(pattern, LED.REPEAT))

    def off(self):
        with self.thread_management_lock:
            if self.thread is not None:
                self.thread.kill()

class _LED_Thread(threading.Thread):
    """
    The LED_Thread is a killable thread for independently handling an LED.

    Naturally, only a single LED should be controlled by any one thread.
    To take control from a thread, you should first kill it with .kill() and
    then create a new one providing the same endpoints.
    """

    def __init__(self, instructions, interval, led_on, led_off):
        if len(instructions) < 1:
            raise ValueError("Instructions must be at least 1 character in length")
        if instructions[0] == LED.REPEAT:
            raise ValueError("First instruction may not be to repeat")

        super().__init__()
        self._instructions = instructions
        self._interval = interval
        self._on = led_on
        self._off = led_off

        self._kill = self.Event()

    def run(self):
        self._off()

        index = 0
        while True:
            index = self._run_instruction(index)

            # If we've run out of instructions
            if index >= len(self._instructions):
                break

            # Wait for the set interval, if kill() is called before or during
            #  the wait, then immediately break, otherwise continue as normal
            if self._kill.wait(self._interval):
                break

        self._off()

    def _run_instruction(self, index):
        instruction = self._instructions[index]
        if instruction == LED.ON:
            self._on()
        elif instruction == LED.OFF:
            self._off()
        elif instruction == LED.REPEAT:
            return self._run_instruction(0)

        return index + 1

    def kill(self):
        self._kill.set()
        # Wait for the kill signal to be recognised
        self.join()

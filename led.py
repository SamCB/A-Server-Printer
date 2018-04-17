import RPi.GPIO as GPIO

import threading
import queue
import time

class _LED_INSTRUCTIONS:
    """A thread-safe, retrieval blocking, single value store

    Use for passing the most recent instruction to the LED thread
    """
    def __init__(self):
        self._queue = queue.LifoQueue(maxsize=1)
        self._lock = threading.Lock()

    def kill(self):
        """Send the KILL_THREAD command over the queue"""
        self.new_instruction(LED.KILL_THREAD, -1)

    def new_instruction(self, code, interval):
        """Remove the previous instruction and pass in this one"""
        with self._lock():
            while True:
                try:
                    self._queue.get()
                except queue.Empty:
                    break

            self._queue.put((code, interval))

    def get_instruction(self, timeout):
        return self._queue.get(timeout=timeout)

class LED:

    ON = '-'
    OFF = ' '
    REPEAT = '*'

    KILL_THREAD = 'KILL_THREAD'

    def __init__(self, pin):
        self.pin = pin

        GPIO.setup(self.pin, GPIO.OUT)
        self._off()

        # Light instructions should
        self.light_instructions = _LED_INSTRUCTIONS()
        self.thread = threading.Thread(
            target=self._light_thread, args=(self.light_instructions)
        )
        self.thread.start()

    def _light_thread(self, light_instructions):
        # a string describing the steps
        instruction_code = LED.OFF
        instruction_index = 1
        instruction_interval = -1
        while True:
            try:
                i = self.light_instructions(timeout=instruction_interval)
                instruction_code, instruction_interval = i
                instruction_index = 0
            except queue.Empty:
                pass

            if instruction_code == LED.KILL_THREAD:
                break

            if instruction_index < len(instruction_code):
                instruction_index = self._run_instruction(
                        instruction_code, instruction_index
                )
            else:
                # There are no more instructions to perform
                # Set interval to -1 so that we sleep when next retrieving
                #  instructions
                instruction_interval = -1

        self._off()

    def _run_instruction(self, code, index):
        instruction = code[index]
        if instruction == LED.ON:
            self._on()
        elif instruction == LED.OFF:
            self._off()
        elif instruction == LED.REPEAT:
            return self._run_instruction(code, 0)

        return index + 1

    def _on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def _off(self):
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


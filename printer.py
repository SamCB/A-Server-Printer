from Adafruit_Thermal import Adafruit_Thermal

import threading
import queue
import time
import re

class _ShutDownPrinter:
    pass

class Printer(Adafruit_Thermal):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._print_queue = queue.Queue()
        self.thread = threading.Thread(target=self._print_from_async_print_queue)
        self.thread.start()

    def _print_from_async_print_queue(self):
        while True:
            try:
                print_func = self._print_queue.get()
                if isinstance(print_func, _ShutDownPrinter):
                    break
                print_func()
            finally:
                self._print_queue.task_done()

    def async_print(self, *args, **kwargs):
        self._print_queue.put(
            lambda: self.print(*args, **kwargs)
        )

    def async_println(self, *args, **kwargs):
        self._print_queue.put(
            lambda: self.println(*args, **kwargs)
        )

    def async_feed(self, *args, **kwargs):
        self._print_queue.put(
            lambda: self.feed(*args, **kwargs)
        )

    def async_wait(self, t):
        self._print_queue.put(lambda: time.sleep(t))

    def batch_print(self, message):
        message = _clean_message(message)
        while message:
            sub, message = message[:180], message[180:]
            self.line_split_print(sub)
            self.async_wait(1)
        self.async_println()
        self.async_feed(3)

    def line_split_print(self, message):
        def find_last_break(message):
            try:
                match = list(re.finditer(r"[ \n\t]", message))
                return match[-1].start(), match[-1].end(), '\n'
            except IndexError:
                return len(message), len(message), ''

        while message:
            break_at, start_at, end = find_last_break(message[:self.maxColumn])
            self.async_print(message[:break_at] + end)
            print(message[:self.maxColumn])
            print(message[:break_at])
            print(break_at, start_at)
            message = message[start_at:]

    def cleanup(self):
        self._print_queue.put(_ShutDownPrinter())
        self.thread.join()

def _clean_message(message):
    """Remove all bytes greater than 128"""
    return ''.join(b if ord(b) < 128 else '?' for b in message)

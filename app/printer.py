from .Adafruit_Thermal import Adafruit_Thermal

import threading
import queue
import time

from .format import format as fmt

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
        # Since flooding the printer with a heap of data causes a backlog
        #  and skipped lines, we print only a handful of characters, then
        #  wait for a second before continuing.
        # Characters and timing is from rough trial and error. They seem
        #  to work.
        message = fmt(message, self.maxColumn)
        while message:
            sub, message = message[:180], message[180:]
            self.async_print(sub)
            self.async_wait(1)
        self.async_println()
        self.async_feed(3)

    def cleanup(self):
        self._print_queue.put(_ShutDownPrinter())
        self.thread.join()


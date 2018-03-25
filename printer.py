from Adafruit_Thermal import Adafruit_Thermal

import threading
import queue
import time

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
                print("NEXT ELEMENT IN QUEUE")
                print(print_func)
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
            lambda: self.println(*args, **kwargs)
        )

    def async_wait(self, t):
        self._print_queue.put(lambda: time.sleep(t))

    def cleanup(self):
        self._print_queue.put(_ShutDownPrinter())
        print("Joining thread")
        self.thread.join()
        print("And we're outa here")

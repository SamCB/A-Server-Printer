import logging
import os

os.makedirs('/home/pi/log', exist_ok=True)
file_handler = logging.FileHandler('/home/pi/log/printer.log')
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(threadName)s - %(name)s | %(message)s",
    handlers=[file_handler, console_handler]
)

def get_logger(name):
    logger = logging.getLogger(name)
    return logger

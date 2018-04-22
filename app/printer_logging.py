import logging
import os

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(threadName)s - %(name)s | %(message)s"
)

formatter = logging.Formatter("%(asctime)s - %(threadName)s - %(name)s | %(message)s")

def get_logger(name):
    logger = logging.getLogger(name)

    os.makedirs('/home/pi/log', exist_ok=True)
    file_handler = logging.FileHandler('/home/pi/log/printer.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    return logger

import logging
import os


def get_log_level():
    log_level = os.environ.get("log_level", logging.INFO)

    if log_level == "debug":
        return logging.DEBUG
    return logging.INFO

logger = logging
LOG_LEVEL = get_log_level()

# log to file and stdout
logger.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    handlers=[
        logging.FileHandler(filename='log.log'),
        logging.StreamHandler()
    ],
    level=LOG_LEVEL)

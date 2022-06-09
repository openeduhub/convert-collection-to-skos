import logging

logger = logging

# log to file and stdout
logger.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    handlers=[
        logging.FileHandler(filename='log.log'),
        logging.StreamHandler()
    ],
    level=logging.INFO)
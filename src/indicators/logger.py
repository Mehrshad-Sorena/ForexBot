import logging
from datetime import datetime
import sys
import os

now = datetime.now()
log_path = 'log/cci/golden_cross_zero/{}-{}-{}-{}-{}-{}.log'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
log_level = 'info'
logger = logging.getLogger()

if not os.path.exists(os.path.dirname(log_path)):
    os.makedirs(os.path.dirname(log_path))

if log_level == 'info':
    logger.setLevel(logging.INFO)
elif log_level == 'warning':
    logger.setLevel(logging.WARNING)
elif log_level == 'debug':
    logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
formatter = logging.Formatter('%(asctime)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


def logs(message):
    logger.info(message)
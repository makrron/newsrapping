"""
This script will define the logs of the API and the scrapping script
"""

import logging
from logging.handlers import RotatingFileHandler


logger = logging.getLogger("NewsCrapping logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler("logbooks/activity.log",
                                   maxBytes=5000000,
                                   backupCount=5)

file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

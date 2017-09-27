import os
import logging
from logging.handlers import RotatingFileHandler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    shandler = logging.StreamHandler()
    shandler.setFormatter(formatter)

    path = os.path.abspath(os.path.dirname(__file__) + "/../") + "/"

    rhandler = RotatingFileHandler(path + name + ".log", mode='a',
                                   maxBytes=1048576, backupCount=5,
                                   encoding=None, delay=0)
    rhandler.setFormatter(formatter)

    logger.addHandler(shandler)
    logger.addHandler(rhandler)

    return logger

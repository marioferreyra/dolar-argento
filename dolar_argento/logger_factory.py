import logging


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    shandler = logging.StreamHandler()
    shandler.setFormatter(formatter)

    logger.addHandler(shandler)

    return logger

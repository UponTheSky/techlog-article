import logging


def get_logger(*, filename: str) -> logging.Logger:
    logger = logging.getLogger(filename)
    logger.setLevel(logging.WARNING)

    return logger

import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging():
    # Create logs directory if non-existent
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger("flaskwebapi")
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    handler = RotatingFileHandler(
        "logs/flaskwebapi.log", maxBytes=100000, backupCount=1
    )
    handler.setLevel(logging.DEBUG)

    # Create a logging format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(handler)

    logger.debug("Logging setup complete")

    return logger

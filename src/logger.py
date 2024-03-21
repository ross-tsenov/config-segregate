import logging

from .settings import settings

__all__ = [
    "logger",
]


def _create_logger() -> logging.Logger:
    """Creates generic logger with the given `logger_name` and `logging_level`"""

    logger = logging.getLogger(settings.logger_name)
    logger.setLevel(settings.logging_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.logging_level)

    formatter = logging.Formatter(
        fmt="%(levelname)s [%(asctime)s %(name)s]: %(message)s",
        datefmt="%m/%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger


logger = _create_logger()
"""Logger that can be imported and be used globally."""

import sys
from enum import Enum
from unittest.mock import Mock


try:
    from loguru import logger
except ModuleNotFoundError:
    logger = Mock()
    logger.trace = print
    logger.debug = print
    logger.info = print
    logger.warning = print
    logger.error = print


class LogLevel(Enum):
    TRACE = 1
    DEBUG = 2
    INFO = 3
    WARNING = 4
    ERROR = 5


def set_log_level(level: LogLevel) -> None:
    logger.remove()
    logger.add(sys.stdout, level=level.name)
    if isinstance(logger, Mock):
        for log_level in LogLevel:
            if log_level.value < level.value:
                setattr(logger, log_level.name.lower(), lambda *args, **kwargs: None)
            else:
                setattr(logger, log_level.name.lower(), print)

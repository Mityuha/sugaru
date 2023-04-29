from unittest.mock import Mock


try:
    from loguru import logger
except ModuleNotFoundError:
    logger = Mock()
    logger.debug = print
    logger.info = print
    logger.warning = print
    logger.error = print

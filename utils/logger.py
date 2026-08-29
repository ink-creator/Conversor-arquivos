import logging
from pathlib import Path
from datetime import datetime
from utils.constants import LOGS_DIR, LOG_FORMAT, LOG_LEVEL

LOGS_DIR.mkdir(exist_ok=True)


def setup_logger(name):
    """Configura logger para módulo específico"""
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(LOG_LEVEL)

    # Handler arquivo
    log_file = LOGS_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Handler console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

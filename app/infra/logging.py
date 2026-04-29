import logging
import logging.handlers
from app.storage.logs import Logs
from app.config import LOG_MODE

logs_access = Logs()

COLOURS = {
    "DEBUG": "\033[36m",
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[41m",
}
RESET = "\033[0m"


class ColourFormatter(logging.Formatter):
    def format(self, record):
        level = record.levelname
        if level in COLOURS:
            record.levelname = f"{COLOURS[level]}{level}{RESET}"
        return super().format(record)


_loggers = {}


def _resolve_log_level():
    mode = LOG_MODE.lower()

    if mode == "off":
        return None  # special case
    elif mode == "on":
        return logging.INFO
    elif mode == "debug":
        return logging.DEBUG
    else:
        raise ValueError(f"LOG_MODE must be 'off', 'on' or 'debug'. Got: '{mode}'")



def get_logger(name: str) -> logging.Logger:
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.propagate = False

    level = _resolve_log_level()

    # -----------------------------------
    # Mode: OFF → disable logger entirely
    # -----------------------------------
    if level is None:
        logger.addHandler(logging.NullHandler())
        _loggers[name] = logger
        return logger

    logger.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(
        ColourFormatter("[%(levelname)s] %(name)s: %(message)s")
    )

    # File handler (always DEBUG to capture full detail)
    file_handler = logging.handlers.RotatingFileHandler(
        logs_access.log_file, maxBytes=2_000_000, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    _loggers[name] = logger
    return logger

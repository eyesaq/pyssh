import logging
import logging.handlers
from config import LOG_LEVEL
from pathlib import Path

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "pyssh.log"

# Colour codes for console output
COLOURS = {
    "DEBUG": "\033[36m",     # Cyan
    "INFO": "\033[32m",      # Green
    "WARNING": "\033[33m",   # Yellow
    "ERROR": "\033[31m",     # Red
    "CRITICAL": "\033[41m",  # Red background
}
RESET = "\033[0m"


class ColourFormatter(logging.Formatter):
    """Adds colour to console logs based on level."""

    def format(self, record):
        level = record.levelname
        if level in COLOURS:
            record.levelname = f"{COLOURS[level]}{level}{RESET}"
        return super().format(record)


# ---------------------------------------------------------------------------
# Logger factory
# ---------------------------------------------------------------------------

_loggers = {}  # cache so handlers aren't duplicated


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger with console + rotating file handlers."""

    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)

    # Apply global log level from config.py
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    logger.propagate = False

    # -----------------------------
    # Console handler
    # -----------------------------
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    console_format = ColourFormatter(
        "[%(levelname)s] %(name)s: %(message)s"
    )
    console_handler.setFormatter(console_format)

    # -----------------------------
    # Rotating file handler
    # -----------------------------
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)  # always capture everything to file

    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    _loggers[name] = logger
    return logger

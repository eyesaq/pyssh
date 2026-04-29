import logging
import logging.handlers
import os
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
    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # avoid double logging

    # -----------------------------
    # Console handler (colourised)
    # -----------------------------
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    console_format = ColourFormatter(
        "[%(levelname)s] %(name)s: %(message)s"
    )
    console_handler.setFormatter(console_format)

    # -----------------------------
    # Rotating file handler
    # -----------------------------
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=2_000_000,   # 2 MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)

    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_format)

    # Attach handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    _loggers[name] = logger
    return logger

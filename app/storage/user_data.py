# Standard imports
from pathlib import Path

# Local application imports
from app.config import APP_NAME
from app.infra.logging import get_logger


log = get_logger(__name__)


class UserDataDir:
    """Centralised access layer for all user data."""

    def __init__(self):
        self.base_dir = self._init_base_dir()

    @staticmethod
    def _init_base_dir() -> Path:
        """
        Create/find and return the user data directory (Windows only).

        Resolves to:
        C:\\Users\\<user>\\AppData\\Local\\PySSH
        """
        path = Path.home() / "AppData" / "Local" / APP_NAME
        path.mkdir(parents=True, exist_ok=True)
        log.info(f"Initialized app data directory @ {path}")
        return path

    def path(self, *parts) -> Path:
        """Resolve a path inside the user data directory."""
        return self.base_dir.joinpath(*parts)

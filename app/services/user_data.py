# Standard imports
from pathlib import Path
import json

# Local application imports
from app.config import APP_NAME


class UserData:
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
        return path

    def path(self, *parts) -> Path:
        """Resolve a path inside the user data directory."""
        return self.base_dir.joinpath(*parts)

    def load_json(self, name: str, default=None):
        """
        Load a JSON file from the user data directory.

        If the file does not exist, the provided default value is returned.
        """
        file = self.path(name)
        if not file.exists():
            return default

        with file.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save_json(self, name: str, data):
        """
        Save structured data as JSON in the user data directory.

        Existing files are overwritten.
        """
        file = self.path(name)
        with file.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

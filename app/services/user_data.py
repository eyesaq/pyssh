from pathlib import Path
import json
from typing import Any, Iterable

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

    def load_json(self, name: str, default: Any = None) -> Any:
        """
        Load a JSON file from the user data directory.

        If the file does not exist, the provided default value is returned.
        """
        file = self.path(name)
        if not file.exists():
            return default

        with file.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save_json(self, name: str, data: Any) -> None:
        """
        Save structured data as JSON in the user data directory.

        Existing files are overwritten.
        """
        file = self.path(name)
        with file.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def append_json_list(self, name: str, items: Iterable[Any]) -> None:
        """
        Append one or more items to a JSON list file.

        If the file does not exist, it is created.
        Raises TypeError if the existing file is not a list.
        """
        data = self.load_json(name, default=[])

        if not isinstance(data, list):
            raise TypeError(f"{name} does not contain a JSON list")

        data.extend(items)
        self.save_json(name, data)

    def update_json_dict(self, name: str, updates: dict) -> None:
        """
        Update a JSON dictionary file with new key-value pairs.

        If the file does not exist, it is created.
        Raises TypeError if the existing file is not a dict.
        """
        data = self.load_json(name, default={})

        if not isinstance(data, dict):
            raise TypeError(f"{name} does not contain a JSON object")

        data.update(updates)
        self.save_json(name, data)

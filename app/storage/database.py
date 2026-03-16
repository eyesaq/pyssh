import sqlite3
from pathlib import Path


class Database:
    _ALLOWED_FIELDS = {
        "ip_address",
        "device_name",
        "username",
        "password_hash",
    }

    def __init__(self, user_data_dir):
        self._db_path: Path = user_data_dir.path("connections.db")
        self._init_database()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    def _init_database(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS connections (
                    ip_address TEXT PRIMARY KEY,
                    device_name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password_hash TEXT NOT NULL
                )
                """
            )

    def get_field_by_ip(self, ip_address: str, field: str):
        if field not in self._ALLOWED_FIELDS:
            raise ValueError(f"Invalid field: {field}")

        with self._connect() as conn:
            row = conn.execute(
                f"SELECT {field} FROM connections WHERE ip_address = ?",
                (ip_address,),
            ).fetchone()

        return row[0] if row else None

    def add_connection(
            self,
            ip_address: str,
            device_name: str,
            username: str,
            password_hash: str,
        ) -> None:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO connections (
                        ip_address,
                        device_name,
                        username,
                        password_hash
                    )
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(ip_address) DO UPDATE SET
                        device_name = excluded.device_name,
                        username = excluded.username,
                        password_hash = excluded.password_hash
                    """,
                    (ip_address, device_name, username, password_hash),
                )


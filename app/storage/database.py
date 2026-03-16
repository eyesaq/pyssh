import sqlite3
from pathlib import Path


class Database:
    _ALLOWED_FIELDS = {
        "ip_address",
        "device_name",
        "username",
        "password",
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
                    password TEXT NOT NULL
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
            password: str,
        ) -> None:
            """Create a new connection record"""
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO connections (
                        ip_address,
                        device_name,
                        username,
                        password
                    )
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(ip_address) DO UPDATE SET
                        device_name = excluded.device_name,
                        username = excluded.username,
                        password = excluded.password
                    """,
                    (ip_address, device_name, username, password),
                )

    def get_all_connections(self) -> list[dict]:
        """Retrieve all connections."""
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT ip_address, device_name, username, password FROM connections"
            ).fetchall()

        return [dict(row) for row in rows]

    def delete_connection_by_ip(self, ip_address: str) -> None:
        """Delete a connection record by IP address."""
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM connections WHERE ip_address = ?",
                (ip_address,),
            )

    def update_field_by_ip(self, ip_address: str, field: str, value: str) -> None:
        """Update a single field for a connection identified by IP address."""
        if field not in self._ALLOWED_FIELDS:
            raise ValueError(f"Invalid field: {field}")

        with self._connect() as conn:
            conn.execute(
                f"UPDATE connections SET {field} = ? WHERE ip_address = ?",
                (value, ip_address),
            )

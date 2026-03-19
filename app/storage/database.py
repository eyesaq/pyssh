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

    def reset_database(self) -> None:
        """Completely reset the database."""
        with self._connect() as conn:
            conn.execute("DROP TABLE IF EXISTS connections")

        self._init_database()

    def get_field_by_ip(self, ip_address: str, field: str):
        if field not in self._ALLOWED_FIELDS:
            raise ValueError(f"Invalid field: {field}")

        with self._connect() as conn:
            row = conn.execute(
                f"SELECT {field} FROM connections WHERE ip_address = ?",
                (ip_address,),
            ).fetchone()

        return row[0] if row else None

    def get_device_info_by_ip(self, ip_address: str) -> tuple | None:
        """Return the full row for a given IP address as a tuple."""
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT ip_address, device_name, username, password
                FROM connections
                WHERE ip_address = ?
                """,
                (ip_address,),
            ).fetchone()

        return row

    def get_all_ip_addresses(self) -> list[str]:
        """Return a list of all IP addresses in the database."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT ip_address FROM connections"
            ).fetchall()

        return [row[0] for row in rows]

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
        """Retrieve all connections"""
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT ip_address, device_name, username, password FROM connections"
            ).fetchall()

        return [dict(row) for row in rows]

    def recreate_database_file(self) -> None:
        """Completely delete the database file and recreate a fresh one."""
        if self._db_path.exists():
            self._db_path.unlink()  # Delete the file

        # Recreate the database with the schema
        self._init_database()

    def delete_by_ip(self, ip_address: str) -> None:
        """Delete a connection record by its IP address."""
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM connections WHERE ip_address = ?",
                (ip_address,),
            )

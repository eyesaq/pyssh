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
        """Create the database table if it doesn't exist"""
        try:
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
        except sqlite3.Error as e:
            raise Exception(f"[DB ERROR] Failed to initialise database: {e}")

    def get_connection_info_by_ip(self, ip_address: str) -> tuple[str, str, str, str] | None:
        """Return the full row for a given IP address as a tuple."""
        try:
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
        except sqlite3.Error as e:
            raise Exception(f"[DB ERROR] Failed to retrieve connection for '{ip_address}': {e}")

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
                    "INSERT INTO connections (ip_address, device_name, username, password) VALUES (?, ?, ?, ?)",
                    (ip_address, device_name, username, password),
                )

    def ip_exists(self, ip_address: str) -> bool:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM connections WHERE ip_address = ?",
                (ip_address,)
            ).fetchone()
        return row is not None

    def get_all_connections(self) -> list[tuple]:
        """Retrieve all connections as a list of tuples."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT ip_address, device_name, username, password FROM connections"
            ).fetchall()

        return rows

    def update_connection_by_ip(
            self,
            old_ip: str,
            new_ip: str | None = None,
            device_name: str | None = None,
            username: str | None = None,
            password: str | None = None,
    ) -> None:
        """
        Update one or more fields for a device identified by its old IP address.
        Allows changing the IP address itself.
        """
        updates = []
        params = []

        if new_ip is not None:
            updates.append("ip_address = ?")
            params.append(new_ip)

        if device_name is not None:
            updates.append("device_name = ?")
            params.append(device_name)

        if username is not None:
            updates.append("username = ?")
            params.append(username)

        if password is not None:
            updates.append("password = ?")
            params.append(password)

        if not updates:
            return  # nothing to update

        params.append(old_ip)

        with self._connect() as conn:
            conn.execute(
                f"UPDATE connections SET {', '.join(updates)} WHERE ip_address = ?",
                params,
            )

    def recreate_database_file(self) -> None:
        """Completely delete the database file and recreate a fresh one."""
        if self._db_path.exists():
            self._db_path.unlink()  # Delete the file

        # Recreate the database with the schema
        self._init_database()

    def delete_connection_by_ip(self, ip_address: str) -> None:
        """Delete a connection record by its IP address."""
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM connections WHERE ip_address = ?",
                (ip_address,),
            )

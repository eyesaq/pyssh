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

    def get_connection_info_by_ip(self, ip_address: str) -> tuple[str, str, str, str] | None:
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
    ) -> bool:
        """Create a new connection record."""
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO connections (ip_address, device_name, username, password) VALUES (?, ?, ?, ?)",
                    (ip_address, device_name, username, password),
                )
            print(f"[DB] Saved connection: '{device_name}'@'{ip_address}'")
            return True
        except sqlite3.IntegrityError:
            print(f"[DB ERROR] Connection '{ip_address}' already exists — not saved")
            return False
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to save connection '{ip_address}': {e}")
            return False

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
    ) -> bool:
        """Update one or more fields for a device. Returns True if successful."""
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
            return True  # nothing to update

        params.append(old_ip)

        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    f"UPDATE connections SET {', '.join(updates)} WHERE ip_address = ?",
                    params,
                )

                if cursor.rowcount == 0:
                    print(f"[DB WARNING] No connection found for '{old_ip}' — nothing updated")
                    return False

            print(f"[DB] Updated connection '{old_ip}'" + (f" -> '{new_ip}'" if new_ip else ""))
            return True

        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to update connection '{old_ip}': {e}")
            return False

    def recreate_database_file(self) -> None:
        """Completely delete the database file and recreate a fresh one."""
        if self._db_path.exists():
            self._db_path.unlink()
        self._init_database()
        print("[DB] Database file recreated")

    def delete_connection_by_ip(self, ip_address: str) -> bool:
        """Delete a connection record by IP address. Returns True if successful."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    "DELETE FROM connections WHERE ip_address = ?",
                    (ip_address,),
                )

                if cursor.rowcount == 0:
                    print(f"[DB WARNING] No connection found for '{ip_address}' — nothing deleted")
                    return False

            print(f"[DB] Deleted connection '{ip_address}'")
            return True

        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to delete connection '{ip_address}': {e}")
            return False

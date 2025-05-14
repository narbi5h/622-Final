import sqlite3
import hashlib
from typing import List, Dict

class User:
    def __init__(self, db_path: str = "walletApp.db"):
        """Initialize with path to SQLite database."""
        self.db_path = db_path

    def _hash_password(self, password: str) -> str:
        """Return a SHA‑256 hash of the given password."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def create(self, name: str, email: str, username: str, password: str):
        """
        Add a new user with credentials.
        Stores the SHA‑256 hash of the password.
        """
        pwd_hash = self._hash_password(password)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO users (name, email, username, password_hash) VALUES (?, ?, ?, ?)",
                (name, email, username, pwd_hash)
            )
            conn.commit()

    def get_by_id(self, user_id: int) -> Dict:
        """Fetch a single user (excluding password) by user_id."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT user_id, name, email, username FROM users WHERE user_id = ?",
                (user_id,)
            )
            row = cur.fetchone()
        return {"user_id": row[0], "name": row[1], "email": row[2], "username": row[3]} if row else {}

    def get_by_username(self, username: str) -> Dict:
        """Fetch full user record (including password_hash) by username."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT user_id, name, email, username, password_hash FROM users WHERE username = ?",
                (username,)
            )
            row = cur.fetchone()
        if not row:
            return {}
        return {
            "user_id":      row[0],
            "name":         row[1],
            "email":        row[2],
            "username":     row[3],
            "password_hash":row[4]
        }

    def authenticate(self, username: str, password: str) -> bool:
        """
        Verify that the provided password matches the stored hash.
        Returns True if credentials are valid.
        """
        user = self.get_by_username(username)
        if not user:
            return False
        return user["password_hash"] == self._hash_password(password)

    def update_email(self, user_id: int, new_email: str):
        """Update the email address for an existing user."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE users SET email = ? WHERE user_id = ?",
                (new_email, user_id)
            )
            conn.commit()

    def update_password(self, user_id: int, new_password: str):
        """Update password for an existing user (stores new hash)."""
        new_hash = self._hash_password(new_password)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE users SET password_hash = ? WHERE user_id = ?",
                (new_hash, user_id)
            )
            conn.commit()

    def delete(self, user_id: int):
        """Remove a user from the database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "DELETE FROM users WHERE user_id = ?",
                (user_id,)
            )
            conn.commit()

    def list_all(self) -> List[Dict]:
        """Return a list of all users (excluding password hashes)."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT user_id, name, email, username FROM users")
            rows = cur.fetchall()
        return [
            {"user_id": r[0], "name": r[1], "email": r[2], "username": r[3]}
            for r in rows
        ]

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

    def create(self, username: str, name:str, email:str, password: str):
        """
        Add a new user with credentials.
        Stores the SHA‑256 hash of the password.
        """
        pwd_hash = self._hash_password(password)
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT user_id FROM users ORDER BY user_id DESC LIMIT 1")
            last_user_id = cur.fetchone()
            if last_user_id and "_" in last_user_id[0]:
                new_user_id = f"user_{int(last_user_id[0].split('_')[1]) + 1}"
            else:
                new_user_id = "user_1"

            conn.execute(
            """
            INSERT INTO users (user_id, username, name, email, password)
            VALUES (?,?, ?, ?, ?)
            """,
            (new_user_id, username, name, email, pwd_hash)
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
                "SELECT user_id, name, email, username, password FROM users WHERE username = ?",
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
            "password":row[4]
        }

    def authenticate(self, username: str, password: str) -> bool:
        """
        Verify that the provided password matches the stored hash.
        Returns True if credentials are valid.
        """
        user = self.get_by_username(username)
        if not user:
            return False
        return user["password"] == self._hash_password(password)

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

    def forgot_password(self, username: str, new_password: str):
        """Allow user to reset password (e.g., forgot password flow)."""
        new_hash = self._hash_password(new_password)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                UPDATE users
                   SET password_hash = ?
                 WHERE username = ?
                """,
                (new_hash, username)
            )
            conn.commit()

    def add_account(self, user_id: int, account_name: str, balance: float):
        """Link a new account to a user."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO accounts (user_id, name, balance)
                VALUES (?, ?, ?)
                """,
                (user_id, account_name, balance)
            )
            conn.commit()

    def close_account(self, account_id: int):
        """Delete an account."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM accounts WHERE account_id = ?", (account_id,))
            conn.commit()

    def freeze_account(self, account_id: int):
        """Freeze an account by setting is_enabled to 0."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                UPDATE accounts
                   SET is_enabled = 0
                 WHERE account_id = ?
                """,
                (account_id,)
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
            {
            "user_id": r[0], 
            "name": r[1],
            "email": r[2],
            "username": r[3]
            }
            for r in rows
        ]
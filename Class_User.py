import sqlite3
from typing import List, Dict
import random
import uuid

class User:
    def __init__(self, db_path: str = "walletApp.db"):
        self.db_path = db_path

    def create(self, username: str, name: str, email: str, password: str):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT user_id FROM users ORDER BY user_id DESC LIMIT 1")
            new_id = str(uuid.uuid4())
              

            conn.execute(
                """
                INSERT INTO users (user_id, username, name, email, password)
                VALUES (?, ?, ?, ?, ?)
                """,
                (new_id, username, name, email, password)
            )
            conn.commit()

    def get_by_id(self, user_id: str) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT user_id, name, email, username FROM users WHERE user_id = ?",
                (user_id,)
            )
            row = cur.fetchone()
        return {"user_id": row[0], "name": row[1], "email": row[2], "username": row[3]} if row else {}

    def get_by_username(self, username: str) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT user_id, name, email, username, password FROM users WHERE username = ?",
                (username,)
            )
            row = cur.fetchone()
        if not row:
            return {}
        return {
            "user_id": row[0],
            "name": row[1],
            "email": row[2],
            "username": row[3],
            "password": row[4]
        }

    def authenticate(self, username: str, password: str) -> bool:
        user = self.get_by_username(username)
        if not user:
            return False
        return user["password"] == password

    def update_email(self, user_id: str, new_email: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE users SET email = ? WHERE user_id = ?",
                (new_email, user_id)
            )
            conn.commit()

    def update_password(self, user_id: str, new_password: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE users SET password = ? WHERE user_id = ?",
                (new_password, user_id)
            )
            conn.commit()

    def forgot_password(self, username: str, new_password: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (new_password, username)
            )
            conn.commit()

    def add_account(self, user_id: str, account_type: str, balance: float):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT account_id FROM account ORDER BY account_id DESC LIMIT 1")
            last_account_id = cur.fetchone()
            if last_account_id:
                new_account_id = f"{int(''.join(filter(str.isdigit, last_account_id[0]))) + 1:08d}"
            else:
                new_account_id = "00000001"

            conn.execute(
                "INSERT INTO account (account_id, user_id, account_type, balance) VALUES (?, ?, ?, ?)",
                (new_account_id, user_id, account_type, balance)
            )
            conn.commit()

    def close_account(self, account_id: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM account WHERE account_id = ?", (account_id,))
            conn.commit()

    def delete(self, user_id: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            conn.commit()

    def list_all(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT user_id, name, email, username FROM users")
            rows = cur.fetchall()
        return [
            {"user_id": r[0], "name": r[1], "email": r[2], "username": r[3]}
            for r in rows
        ]

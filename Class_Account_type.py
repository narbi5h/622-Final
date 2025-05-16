import sqlite3
from typing import List, Dict

class AccountType:
    def __init__(self, db_path: str = "walletApp.db"):
        """
        Manages the `account_type` table, which should have columns:
          - account_type       INTEGER PRIMARY KEY
          - name          TEXT    NOT NULL UNIQUE
          - description   TEXT
          - is_enabled    INTEGER NOT NULL DEFAULT 1  -- 1=enabled, 0=disabled
        """
        self.db_path = db_path

    def add_account_type(self, type_name: str, description: str = ""):
        """INSERT a new account type (enabled by default)."""
        sql = """
        INSERT INTO account_type (type_name)
        VALUES (?, ?)
        """
        self._run(sql, (type_name))

    def list_all(self) -> List[Dict]:
        """RETURN all account types, including their enabled/disabled status."""
        sql = """
        SELECT account_type, type_name, is_enabled
          FROM account_type
        """
        return self._fetchall(sql)
        # sql = """
        # SELECT account_type, type_name, is_enabled
        #  FROM account_types"

        # """
        # return self._fetchall(sql)

    def change_account_type_name(self, account_type: int, new_name: str):
        """UPDATE the name of an existing account type."""
        sql = """
        UPDATE account_type
           SET name = ?
         WHERE account_type = ?
        """
        self._run(sql, (new_name, account_type))

    def get_account_details(self, account_type: int) -> Dict:
        """SELECT and RETURN details for a single account type by ID."""
        sql = """
        SELECT account_type, type_description, is_enabled
          FROM account_type
         WHERE account_type = ?
        """
        return self._fetchone(sql, (account_type,))

    def disable_account(self, account_type: int):
        """SET is_enabled = 0 for the given account type."""
        sql = """
        UPDATE account_type
           SET is_enabled = 0
         WHERE account_type = ?
        """
        self._run(sql, (account_type,))

    def enable_account(self, account_type: int):
        """SET is_enabled = 1 for the given account type."""
        sql = """
        UPDATE account_type
           SET is_enabled = 1
         WHERE account_type = ?
        """
        self._run(sql, (account_type,))

    # ────────────────────────────────────────────────────────────────────────────
    # Private helpers
    # ────────────────────────────────────────────────────────────────────────────

    def _run(self, sql: str, params: tuple = ()):
        """Execute INSERT/UPDATE/DELETE and commit."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(sql, params)
            conn.commit()

    def _fetchone(self, sql: str, params: tuple = ()) -> Dict:
        """Execute SELECT and return a single row as a dict (or empty dict)."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(sql, params)
            row = cur.fetchone()
            if not row:
                return {}
            cols = [d[0] for d in cur.description]
            return dict(zip(cols, row))

    def _fetchall(self, sql: str, params: tuple = ()) -> List[Dict]:
        """Execute SELECT and return all rows as a list of dicts."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(sql, params)
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in rows]
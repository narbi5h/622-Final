import sqlite3
from typing import List, Dict
import os
from datetime import datetime

class Class_Account:
    def __init__(self, db_path: str = "walletApp.db"):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def open_account(self, user_id: int, account_type: str, balance: float) -> str:
        with self._connect() as conn:
            cur = conn.execute("SELECT account_id FROM account ORDER BY account_id DESC LIMIT 1")
            last = cur.fetchone()
            if last:
                last_id = last[0]
                last_num = int(''.join(filter(str.isdigit, last_id)))
                new_id = f"ACCT{last_num + 1:03d}"
            else:
                new_id = "ACCT001"
            
            if account_type.lower() == "ck":
                account_type = "1"
            elif account_type.lower() == "sv":
                account_type = "2"
            else:
                raise ValueError("Invalid account type. Use 'ck' for checking or 'sv' for savings.")

            conn.execute("""
                INSERT INTO account (account_id, user_id, account_type, balance)
                VALUES (?, ?, ?, ?)
            """, (new_id, user_id, account_type, balance))
            conn.commit()
            return new_id


    def close_account(self, account_id: str) -> bool:
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM account WHERE account_id = ?", (account_id,))
            conn.commit()
            return cur.rowcount > 0

    def read_records(self, lines: list[str]):
        records = [line.split(",") for line in lines]
        records = [(float(a), datetime.fromisoformat(d), c, n) for a, d, c, n in records]
        self.incomes = [a for a in records if a[0] > 0]
        self.expenses = [-a[0] for a in records if a[0] < 0]

    def switch_accounts(self, user_id: str) -> str:
        accounts = self.list_accounts(user_id)
        if not accounts:
            print("No accounts available.")
            return None

        print("Available accounts:")
        for i, acc in enumerate(accounts):
            print(f"{i + 1}. ID: {acc['account_id']} | Balance: {acc['balance']}")
        index = int(input("Select account number: ")) - 1
        return accounts[index]["account_id"]

    def list_accounts(self, user_id: str) -> List[Dict]:
        with self._connect() as conn:
            cur = conn.execute("SELECT account_id, balance FROM account WHERE user_id = ?", (user_id,))
            rows = cur.fetchall()
            return [{"account_id": row[0], "balance": row[1]} for row in rows]

    def get_account(self, account_id: str) -> Dict:
        with self._connect() as conn:
            cur = conn.execute("SELECT account_id, user_id, account_type, balance FROM account WHERE account_id = ?", (account_id,))
            row = cur.fetchone()
            if row:
                return {
                    "account_id": row[0],
                    "user_id": row[1],
                    "account_type": row[2],
                    "balance": row[3]
                }
            return {}

    def edit_balance(self, account_id: str, new_balance: float):
        with self._connect() as conn:
            conn.execute("UPDATE account SET balance = ? WHERE account_id = ?", (new_balance, account_id))
            conn.commit()

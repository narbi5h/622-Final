import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

class Transaction:
    def __init__(self, db_path: str = "walletApp.db"):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def list_all(self, account_id: str):
        with self._connect() as conn:
            cur = conn.execute("""
                SELECT amount, timestamp, type_id, sub_category_id
                FROM transactions
                WHERE account_id = ?
                ORDER BY timestamp
            """, (account_id,))
            return cur.fetchall()

    def add_income(self, account_id: str, amount: float, category: str = "Other", note: str = ""):
        self._add_transaction(account_id, amount, category, note, type_id=1)

    def add_expense(self, account_id: str, amount: float, category: str = "Other", note: str = ""):
        current_balance = self._get_balance(account_id)
        if amount > current_balance:
            raise ValueError("Not enough funds.")
        self._add_transaction(account_id, -abs(amount), category, note, type_id=2)

    def _add_transaction(self, account_id: str, amount: float, category: str, note: str, type_id: int):
        timestamp = datetime.now(ZoneInfo("US/Pacific")).strftime("%Y-%m-%d %H:%M:%S")

        with self._connect() as conn:
            cur = conn.execute("SELECT transaction_id FROM transactions ORDER BY transaction_id DESC LIMIT 1")
            last = cur.fetchone()
            if last:
                last_id = last[0]
                last_num = int(''.join(filter(str.isdigit, last_id)))
                new_id = f"TXN{last_num + 1:03d}"
            else:
                new_id = "TXN001"

            cur = conn.execute("""
                SELECT sub_category_id FROM categories
                WHERE name = ? AND transaction_type_id = ?
            """, (category, type_id))
            row = cur.fetchone()
            sub_category_id = category
            # if last:
            #     last_sub_id = last[0]
            #     last_num = int(''.join(filter(str.isdigit, last_sub_id)))
            #     sub_category_id = f"SC{last_num + 1:03d}"

            conn.execute("""
                INSERT INTO transactions (transaction_id, account_id, type_id, sub_category_id, amount, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (new_id, account_id, type_id, sub_category_id, amount, timestamp))

            # Update account balance
            new_balance = self._get_balance(account_id) + amount
            conn.execute("UPDATE account SET balance = ? WHERE account_id = ?", (new_balance, account_id))
            conn.commit()

    def _get_balance(self, account_id: str) -> float:
        with self._connect() as conn:
            cur = conn.execute("SELECT balance FROM account WHERE account_id = ?", (account_id,))
            row = cur.fetchone()
            return row[0] if row else 0.0

    def update_amount(self, account_id: str):
        with self._connect() as conn:
            cur = conn.execute("""
                SELECT transaction_id, amount, timestamp, type_id
                FROM transactions
                WHERE account_id = ?
                ORDER BY timestamp
            """, (account_id,))
            transactions = cur.fetchall()

            for i, txn in enumerate(transactions):
                print(f"{i}: ID={txn[0]}, Amount={txn[1]}, Time={txn[2]}, Type={txn[3]}")

            idx = int(input("Enter index of record to update: "))
            new_amount = float(input("Enter new amount: "))
            txn_id = transactions[idx][0]
            old_amount = transactions[idx][1]

            conn.execute("UPDATE transactions SET amount = ? WHERE transaction_id = ?", (new_amount, txn_id))

            # Recalculate balance
            balance_change = new_amount - old_amount
            current_balance = self._get_balance(account_id)
            conn.execute("UPDATE account SET balance = ? WHERE account_id = ?", (current_balance + balance_change, account_id))
            conn.commit()

    def transfer(self, from_account_id: str, to_account_id: str, amount: float, note: str = ""):
        if amount > self._get_balance(from_account_id):
            return "Not enough funds to transfer."

        # Subtract from source
        self._add_transaction(from_account_id, -abs(amount), category="Transfer", note=note, type_id=2)

        # Add to target
        self._add_transaction(to_account_id, abs(amount), category="Transfer", note=f"Received from account {from_account_id}", type_id=1)

        return "Transfer complete."

import sqlite3
from typing import List, Dict

class TRANSACTION_TYPE:
    def __init__(self, db_path: str = "walletApp.db"):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def LIST_ALL(self) -> List[Dict]:
        with self._connect() as conn:
            cur = conn.execute("SELECT transaction_type_id, category_name FROM TRANSACTION_TYPE")
            return [{"type_id": row[0], "category_name": row[1]} for row in cur.fetchall()]

    def UPDATE_NAME(self, type_id: int, new_name: str) -> str:
        with self._connect() as conn:
            cur = conn.execute(
                "UPDATE TRANSACTION_TYPE SET category_name = ? WHERE transaction_type_id = ?",
                (new_name, type_id)
            )
            conn.commit()
            return f"Updated type_id {type_id} to new name '{new_name}'" if cur.rowcount > 0 else "Type ID not found"

    def DELETE_TYPE(self, type_id: int) -> str:
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM TRANSACTION_TYPE WHERE transaction_type_id = ?", (type_id,))
            conn.commit()
            return f"Deleted type_id {type_id}" if cur.rowcount > 0 else "Type ID not found"

    def SEARCH(self, keyword: str) -> List[Dict]:
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT transaction_type_id, category_name FROM TRANSACTION_TYPE WHERE category_name LIKE ?",
                (f"%{keyword}%",)
            )
            return [{"type_id": row[0], "category_name": row[1]} for row in cur.fetchall()]

    def ADD(self, type_id: int, category_name: str) -> str:
        with self._connect() as conn:
            cur = conn.execute("SELECT 1 FROM TRANSACTION_TYPE WHERE transaction_type_id = ?", (type_id,))
            if cur.fetchone():
                return f"Type ID {type_id} already exists"
            conn.execute(
                "INSERT INTO TRANSACTION_TYPE (transaction_type_id, category_name) VALUES (?, ?)",
                (type_id, category_name)
            )
            conn.commit()
            return f"Added new transaction type with type_id {type_id} and category_name '{category_name}'"

    def GROUP(self) -> Dict[str, List[Dict]]:
        all_types = self.LIST_ALL()
        grouped = {}

        def helper(index):
            if index >= len(all_types):
                return
            item = all_types[index]
            key = item["category_name"][0].upper()
            grouped.setdefault(key, []).append(item)
            helper(index + 1)

        helper(0)
        return grouped
import sqlite3
from datetime import datetime
from typing import List, Dict, Any

class exportLogs:
    def __init__(self, db_path: str = "wallet.db"):
        self.db_path = db_path
        self.logs = self.loadLogsWithBalance()

    def loadLogsWithBalance(self) -> List[Dict[str, Any]]:
        """Join exportLogs with ACCOUNT to include balance for sorting."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = """
        SELECT e.export_id, e.account_id, e.timestamp, e.file_path, a.balance
        FROM EXPORT_LOGS e
        JOIN ACCOUNT a ON e.account_id = a.account_id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def sortByIndex(self) -> List[Dict[str, Any]]:
        return sorted(self.logs, key=lambda x: x['export_id'])

    def sortByTimestamp(self) -> List[Dict[str, Any]]:
        return sorted(self.logs, key=lambda x: datetime.strptime(x['timestamp'], "%Y-%m-%d %H:%M:%S"))

    def sortByMaxExpense(self) -> List[Dict[str, Any]]:
        """Sort logs by associated account balance descending."""
        return sorted(self.logs, key=lambda x: x['balance'], reverse=True)

    def sortByMinExpense(self) -> List[Dict[str, Any]]:
        """Sort logs by associated account balance ascending."""
        return sorted(self.logs, key=lambda x: x['balance'])

    def findByIndex(self, export_id: int) -> Dict[str, Any]:
        for log in self.logs:
            if log['export_id'] == export_id:
                return log
        return {"error": f"No export log with ID {export_id}"}

    def findByAmount(self, balance: float) -> List[Dict[str, Any]]:
        """Find logs where the associated account's balance equals the amount."""
        results = [log for log in self.logs if log['balance'] == balance]
        return results if results else [{"error": f"No logs found with balance {balance}"}]

# if __name__ == "__main__":
#     logs = exportLogs("wallet.db")

#     print("=== SORTED BY TIMESTAMP ===")
#     for log in logs.sortByTimestamp():
#         print(log)

#     print("\n=== FIND BY EXPORT ID ===")
#     print(logs.findByIndex(2))

#     print("\n=== SORT BY MAX BALANCE ===")
#     for log in logs.sortByMaxExpense():
#         print(log)

#     print("\n=== FIND BY BALANCE ===")
#     balance = float(input("Enter balance to search by: "))
#     print(logs.findByAmount(balance))
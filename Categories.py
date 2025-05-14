import sqlite3
from typing import List, Dict, Any

class Categories:
    def __init__(self, db_path: str = "walletApp.db"):
        self.db_path = db_path

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def add(self, name: str) -> Dict[str, Any]:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO CATEGORIES (name) VALUES (?)", (name,))
            conn.commit()
            return {"success": f"Category '{name}' added."}
        except sqlite3.Error as e:
            return {"error": str(e)}
        finally:
            conn.close()

    def update(self, category_id: int, new_name: str) -> Dict[str, Any]:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE CATEGORIES SET name = ? WHERE category_id = ?", (new_name, category_id))
            conn.commit()
            if cursor.rowcount == 0:
                return {"error": f"No category with ID {category_id}"}
            return {"success": f"Category ID {category_id} updated to '{new_name}'."}
        except sqlite3.Error as e:
            return {"error": str(e)}
        finally:
            conn.close()

    def delete(self, category_id: int) -> Dict[str, Any]:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM CATEGORIES WHERE category_id = ?", (category_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return {"error": f"No category with ID {category_id}"}
            return {"success": f"Category ID {category_id} deleted."}
        except sqlite3.Error as e:
            return {"error": str(e)}
        finally:
            conn.close()

    def view(self) -> List[Dict[str, Any]]:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM CATEGORIES")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def sort(self) -> List[Dict[str, Any]]:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM CATEGORIES ORDER BY name ASC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()


# if __name__ == "__main__":
#     cat = Categories("walletApp.db")

#     # Example usage
#     print(cat.add("Books"))
#     print(cat.add("Groceries"))
#     print(cat.view())
#     print(cat.update(1, "E-Books"))
#     print(cat.delete(2))
#     print(cat.sort())
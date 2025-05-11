import sqlite3
from sqlite3 import Error

class SQLiteHelper:
    def __init__(self, db_file):
        """初始化SQLiteHelper並連接到指定的資料庫"""
        self.connection = None
        try:
            self.connection = sqlite3.connect(db_file)
            print(f"成功連接到SQLite資料庫: {db_file}")
        except Error as e:
            print(f"無法連接到資料庫: {e}")

    def execute_query(self, query, params=None):
        """執行一個SQL查詢"""
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            print("查詢執行成功")
        except Error as e:
            print(f"查詢失敗: {e}")

    def execute_read_query(self, query, params=None):
        """執行一個讀取的SQL查詢，並返回結果"""
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"查詢失敗: {e}")
            return None

    def close_connection(self):
        """關閉資料庫連接"""
        if self.connection:
            self.connection.close()
            print("資料庫連接已關閉")

# 使用範例
if __name__ == "__main__":
    db = SQLiteHelper("test.db")
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT
    );
    """
    db.execute_query(create_table_query)
    
    insert_query = "INSERT INTO users (name, age, gender) VALUES (?, ?, ?)"
    db.execute_query(insert_query, ("John Doe", 28, "Male"))
    
    select_query = "SELECT * FROM users"
    users = db.execute_read_query(select_query)
    for user in users:
        print(user)
    
    db.close_connection()

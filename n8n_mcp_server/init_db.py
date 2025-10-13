"""Initialize the demo database"""
import sqlite3

def init_database():
    """創建示範資料庫和表格"""
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    
    # 創建示範用的 users 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER
        )
    """)
    
    # 插入示範資料
    cursor.execute("""
        INSERT OR IGNORE INTO users (name, email, age) VALUES
        ('Alice', 'alice@example.com', 30),
        ('Bob', 'bob@example.com', 25),
        ('Charlie', 'charlie@example.com', 35)
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()

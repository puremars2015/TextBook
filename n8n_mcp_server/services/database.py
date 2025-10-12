"""Shared database service"""
from typing import Optional
import sqlite3


class DatabaseService:
    """共享的資料庫服務 (Singleton 模式)"""
    
    _instance: Optional['DatabaseService'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self.connection = None
        self._initialized = True
    
    def connect(self, db_path: str):
        """建立資料庫連接"""
        if self.connection is None:
            self.connection = sqlite3.connect(db_path, check_same_thread=False)
    
    def query(self, sql: str, params: tuple = ()):
        """執行查詢
        
        Args:
            sql: SQL 查詢語句
            params: 查詢參數
            
        Returns:
            查詢結果列表
        """
        if self.connection is None:
            raise RuntimeError("Database not connected")
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()
    
    def execute(self, sql: str, params: tuple = ()):
        """執行寫入操作
        
        Args:
            sql: SQL 語句
            params: 參數
            
        Returns:
            影響的行數
        """
        if self.connection is None:
            raise RuntimeError("Database not connected")
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        self.connection.commit()
        return cursor.rowcount
    
    def close(self):
        """關閉連接"""
        if self.connection:
            self.connection.close()
            self.connection = None

"""Database operations endpoint"""
from endpoints.base import BaseEndpoint
from services.database import DatabaseService
from typing import List, Dict, Any


class DatabaseOpsEndpoint(BaseEndpoint):
    """資料庫操作 endpoint"""
    
    def __init__(self):
        super().__init__(path="/database_ops")
        self.db_service = DatabaseService()
    
    def get_name(self) -> str:
        return "database_operations"
    
    def get_description(self) -> str:
        return "提供資料庫查詢、插入、更新等操作"
    
    def register_tools(self) -> List[Dict[str, Any]]:
        """註冊 tools"""
        
        def query_database(sql: str) -> str:
            """執行資料庫查詢
            
            Args:
                sql: SQL 查詢語句
                
            Returns:
                查詢結果的字串表示
            """
            try:
                results = self.db_service.query(sql)
                return str(results)
            except Exception as e:
                return f"Error: {str(e)}"
        
        def insert_data(table: str, data: dict) -> str:
            """插入資料到資料庫
            
            Args:
                table: 資料表名稱
                data: 要插入的資料 (dict)
                
            Returns:
                執行結果訊息
            """
            try:
                columns = ', '.join(data.keys())
                placeholders = ', '.join(['?' for _ in data])
                sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                
                rows = self.db_service.execute(sql, tuple(data.values()))
                return f"Inserted {rows} row(s)"
            except Exception as e:
                return f"Error: {str(e)}"
        
        def update_data(table: str, data: dict, condition: str) -> str:
            """更新資料庫資料
            
            Args:
                table: 資料表名稱
                data: 要更新的資料 (dict)
                condition: WHERE 條件
                
            Returns:
                執行結果訊息
            """
            try:
                set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
                sql = f"UPDATE {table} SET {set_clause} WHERE {condition}"
                
                rows = self.db_service.execute(sql, tuple(data.values()))
                return f"Updated {rows} row(s)"
            except Exception as e:
                return f"Error: {str(e)}"
        
        return [
            {'func': query_database},
            {'func': insert_data},
            {'func': update_data}
        ]

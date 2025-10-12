"""File handler endpoint"""
from endpoints.base import BaseEndpoint
from typing import List, Dict, Any
import os


class FileHandlerEndpoint(BaseEndpoint):
    """檔案處理 endpoint"""
    
    def __init__(self):
        super().__init__(path="/file_handler")
    
    def get_name(self) -> str:
        return "file_operations"
    
    def get_description(self) -> str:
        return "提供檔案讀取、寫入等操作"
    
    def register_tools(self) -> List[Dict[str, Any]]:
        """註冊 tools"""
        
        def read_file(filepath: str) -> str:
            """讀取檔案內容
            
            Args:
                filepath: 檔案路徑
                
            Returns:
                檔案內容或錯誤訊息
            """
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                return f"Error: {str(e)}"
        
        def write_file(filepath: str, content: str) -> str:
            """寫入檔案
            
            Args:
                filepath: 檔案路徑
                content: 要寫入的內容
                
            Returns:
                執行結果訊息
            """
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"Successfully wrote to {filepath}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        def list_files(directory: str) -> str:
            """列出目錄中的檔案
            
            Args:
                directory: 目錄路徑
                
            Returns:
                檔案列表或錯誤訊息
            """
            try:
                files = os.listdir(directory)
                return '\n'.join(files)
            except Exception as e:
                return f"Error: {str(e)}"
        
        return [
            {'func': read_file},
            {'func': write_file},
            {'func': list_files}
        ]

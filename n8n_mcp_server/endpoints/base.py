"""Base endpoint class for all MCP endpoints"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseEndpoint(ABC):
    """Endpoint 基礎類別"""
    
    def __init__(self, path: str):
        self.path = path
        self.tools = []
        
    @abstractmethod
    def register_tools(self) -> List[Dict[str, Any]]:
        """註冊此 endpoint 的 tools
        
        Returns:
            List of tool definitions
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """取得 endpoint 名稱"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """取得 endpoint 描述"""
        pass

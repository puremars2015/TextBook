"""Endpoint manager for managing multiple MCP endpoints"""
from typing import Dict, Optional
from mcp.server.fastmcp import FastMCP
from endpoints.base import BaseEndpoint


class EndpointManager:
    """管理多個 MCP endpoint"""
    
    def __init__(self):
        self.endpoints: Dict[str, BaseEndpoint] = {}
        self.mcp_servers: Dict[str, FastMCP] = {}
    
    def register_endpoint(self, endpoint: BaseEndpoint) -> bool:
        """註冊新的 endpoint
        
        Args:
            endpoint: BaseEndpoint 實例
            
        Returns:
            註冊是否成功
        """
        if endpoint.path in self.endpoints:
            return False
            
        # 創建 FastMCP 實例
        mcp = FastMCP(endpoint.get_name())
        
        # 註冊 tools
        tools = endpoint.register_tools()
        for tool in tools:
            mcp.tool()(tool['func'])
        
        self.endpoints[endpoint.path] = endpoint
        self.mcp_servers[endpoint.path] = mcp
        
        return True
    
    def unregister_endpoint(self, path: str) -> bool:
        """移除 endpoint
        
        Args:
            path: endpoint 路徑
            
        Returns:
            移除是否成功
        """
        if path not in self.endpoints:
            return False
            
        del self.endpoints[path]
        del self.mcp_servers[path]
        
        return True
    
    def get_endpoint(self, path: str) -> Optional[FastMCP]:
        """取得指定 endpoint 的 MCP server
        
        Args:
            path: endpoint 路徑
            
        Returns:
            FastMCP 實例或 None
        """
        return self.mcp_servers.get(path)
    
    def list_endpoints(self) -> Dict[str, str]:
        """列出所有已註冊的 endpoint
        
        Returns:
            {path: description} 字典
        """
        return {
            path: endpoint.get_description()
            for path, endpoint in self.endpoints.items()
        }

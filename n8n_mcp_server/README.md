# Multi-Endpoint MCP Server 規格文件

## 概述

這是一個基於 FastMCP 2.0 的多端點 MCP Server 架構,支援在單一 server 下動態管理多個獨立功能的 endpoint,透過 streamable HTTP 協議通訊。

## 架構設計

### 核心概念

```
┌─────────────────────────────────────┐
│         MCP Server (HTTP)           │
├─────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐        │
│  │ Endpoint │  │ Endpoint │  ...   │
│  │ Manager  │  │ Registry │        │
│  └──────────┘  └──────────┘        │
├─────────────────────────────────────┤
│         Service Layer               │
│  ┌──────────┐  ┌──────────┐        │
│  │ Database │  │  Utils   │        │
│  │ Service  │  │ Service  │        │
│  └──────────┘  └──────────┘        │
├─────────────────────────────────────┤
│          Endpoints                  │
│  /database_ops  /file_handler       │
└─────────────────────────────────────┘
```

### 專案結構

```
mcp-server/
├── main.py                  # 主程式入口
├── server/
│   ├── __init__.py
│   ├── manager.py          # Endpoint 管理器
│   └── registry.py         # Endpoint 註冊器
├── services/               # 共享 service 層
│   ├── __init__.py
│   ├── database.py         # 資料庫服務
│   └── utils.py            # 工具函數服務
├── endpoints/              # 各功能 endpoint
│   ├── __init__.py
│   ├── base.py            # Endpoint 基礎類別
│   ├── database_ops.py    # 資料庫操作 endpoint
│   └── file_handler.py    # 檔案處理 endpoint
├── requirements.txt
└── README.md
```

## 核心組件規格

### 1. Endpoint 基礎類別 (`endpoints/base.py`)

每個 endpoint 必須繼承此基礎類別:

```python
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
```

### 2. Endpoint 管理器 (`server/manager.py`)

負責管理所有 endpoint 的生命週期:

```python
from typing import Dict, Optional
from fastmcp import FastMCP
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
```

### 3. Service 層範例 (`services/database.py`)

共享的資料庫服務:

```python
from typing import Optional
import sqlite3

class DatabaseService:
    """共享的資料庫服務"""
    
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
        """執行查詢"""
        if self.connection is None:
            raise RuntimeError("Database not connected")
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()
    
    def execute(self, sql: str, params: tuple = ()):
        """執行寫入操作"""
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
```

### 4. Endpoint 實作範例

#### Database Operations Endpoint (`endpoints/database_ops.py`)

```python
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
```

#### File Handler Endpoint (`endpoints/file_handler.py`)

```python
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
```

### 5. 主程式 (`main.py`)

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from server.manager import EndpointManager
from endpoints.database_ops import DatabaseOpsEndpoint
from endpoints.file_handler import FileHandlerEndpoint
from services.database import DatabaseService
import uvicorn

# 初始化
app = FastAPI(title="Multi-Endpoint MCP Server")
manager = EndpointManager()

# 初始化共享服務
db_service = DatabaseService()
db_service.connect("app.db")  # 連接資料庫

@app.on_event("startup")
async def startup_event():
    """伺服器啟動時註冊所有 endpoint"""
    
    # 註冊 database operations endpoint
    db_endpoint = DatabaseOpsEndpoint()
    manager.register_endpoint(db_endpoint)
    
    # 註冊 file handler endpoint
    file_endpoint = FileHandlerEndpoint()
    manager.register_endpoint(file_endpoint)
    
    print("Registered endpoints:")
    for path, desc in manager.list_endpoints().items():
        print(f"  {path}: {desc}")

@app.on_event("shutdown")
async def shutdown_event():
    """伺服器關閉時清理資源"""
    db_service.close()

@app.post("/{endpoint_path:path}")
async def handle_mcp_request(endpoint_path: str, request: Request):
    """處理 MCP 請求
    
    Args:
        endpoint_path: endpoint 路徑
        request: FastAPI Request 物件
        
    Returns:
        StreamingResponse with MCP protocol data
    """
    # 正規化路徑
    if not endpoint_path.startswith('/'):
        endpoint_path = '/' + endpoint_path
    
    # 取得對應的 MCP server
    mcp_server = manager.get_endpoint(endpoint_path)
    
    if mcp_server is None:
        return {"error": f"Endpoint not found: {endpoint_path}"}
    
    # 取得請求 body
    body = await request.json()
    
    # 使用 FastMCP 處理請求
    # 這裡需要根據 FastMCP 2.0 的實際 API 調整
    response = await mcp_server.handle_request(body)
    
    return StreamingResponse(
        response,
        media_type="application/json"
    )

@app.get("/endpoints")
async def list_endpoints():
    """列出所有可用的 endpoint"""
    return manager.list_endpoints()

@app.post("/admin/register")
async def register_endpoint(endpoint_config: dict):
    """動態註冊新的 endpoint
    
    Args:
        endpoint_config: endpoint 配置
        
    Returns:
        註冊結果
    """
    # 這裡可以實作動態載入 endpoint 的邏輯
    return {"message": "Dynamic registration not implemented yet"}

@app.delete("/admin/unregister/{endpoint_path:path}")
async def unregister_endpoint(endpoint_path: str):
    """移除 endpoint
    
    Args:
        endpoint_path: endpoint 路徑
        
    Returns:
        移除結果
    """
    if not endpoint_path.startswith('/'):
        endpoint_path = '/' + endpoint_path
        
    success = manager.unregister_endpoint(endpoint_path)
    
    if success:
        return {"message": f"Endpoint {endpoint_path} unregistered"}
    else:
        return {"error": f"Endpoint not found: {endpoint_path}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 使用方式

### 1. 安裝依賴

```bash
pip install fastmcp fastapi uvicorn
```

### 2. 啟動伺服器

```bash
python main.py
```

### 3. 測試 Endpoint

```bash
# 列出所有 endpoint
curl http://localhost:8000/endpoints

# 呼叫 database operations
curl -X POST http://localhost:8000/database_ops \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "query_database", "arguments": {"sql": "SELECT * FROM users"}}}'

# 呼叫 file handler
curl -X POST http://localhost:8000/file_handler \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "read_file", "arguments": {"filepath": "test.txt"}}}'
```

### 4. 新增自訂 Endpoint

創建新的 endpoint 檔案 `endpoints/my_endpoint.py`:

```python
from endpoints.base import BaseEndpoint
from typing import List, Dict, Any

class MyEndpoint(BaseEndpoint):
    def __init__(self):
        super().__init__(path="/my_feature")
    
    def get_name(self) -> str:
        return "my_feature"
    
    def get_description(self) -> str:
        return "我的自訂功能"
    
    def register_tools(self) -> List[Dict[str, Any]]:
        def my_tool(param: str) -> str:
            """我的工具函數"""
            return f"處理: {param}"
        
        return [{'func': my_tool}]
```

在 `main.py` 的 `startup_event` 中註冊:

```python
from endpoints.my_endpoint import MyEndpoint

@app.on_event("startup")
async def startup_event():
    # ... 其他註冊
    
    my_endpoint = MyEndpoint()
    manager.register_endpoint(my_endpoint)
```

## 擴展性考量

### 1. 錯誤處理
- Server 層級錯誤會導致整個伺服器重啟
- Endpoint 層級錯誤僅影響該 endpoint 的請求

### 2. 共享資源模式
- 使用 Singleton 模式管理資料庫連接
- Service 層可以擴展更多共享功能

### 3. 動態載入
- 預留了動態註冊/移除 endpoint 的 API
- 可以透過 `/admin/register` 和 `/admin/unregister` 管理

### 4. 監控與日誌
建議加入:
- 請求日誌
- 效能監控
- 錯誤追蹤

## 注意事項

1. **FastMCP 2.0 API**: 此 spec 中的 `mcp_server.handle_request()` 需要根據實際 FastMCP 2.0 API 調整
2. **安全性**: 目前未實作權限控制,生產環境需要加入認證機制
3. **錯誤恢復**: Server 重啟會中斷所有連接,建議加入健康檢查機制
4. **資料庫連接池**: 生產環境建議使用連接池管理資料庫連接

## 未來改進方向

- [ ] 加入認證與授權機制
- [ ] 實作完整的動態載入功能
- [ ] 加入配置檔支援
- [ ] 提供更完整的錯誤處理
- [ ] 加入監控與日誌系統
- [ ] 支援 endpoint 版本管理
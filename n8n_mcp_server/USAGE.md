# Multi-Endpoint MCP Server 使用指南

## 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 初始化資料庫 (可選)

```bash
python init_db.py
```

### 3. 啟動伺服器

```bash
python app.py
```

或使用 uvicorn:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

伺服器將在 `http://localhost:8000` 啟動。

## API 端點說明

### 基本資訊端點

#### GET /
查看伺服器基本資訊
```bash
curl http://localhost:8000/
```

#### GET /endpoints
列出所有已註冊的 endpoint
```bash
curl http://localhost:8000/endpoints
```

### MCP Endpoint

#### POST /database_ops
資料庫操作 endpoint

範例 - 查詢資料：
```bash
curl -X POST http://localhost:8000/database_ops \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "query_database",
      "arguments": {
        "sql": "SELECT * FROM users"
      }
    }
  }'
```

範例 - 插入資料：
```bash
curl -X POST http://localhost:8000/database_ops \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "insert_data",
      "arguments": {
        "table": "users",
        "data": {
          "name": "David",
          "email": "david@example.com",
          "age": 28
        }
      }
    }
  }'
```

#### POST /file_handler
檔案處理 endpoint

範例 - 讀取檔案：
```bash
curl -X POST http://localhost:8000/file_handler \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "read_file",
      "arguments": {
        "filepath": "README.md"
      }
    }
  }'
```

範例 - 寫入檔案：
```bash
curl -X POST http://localhost:8000/file_handler \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "write_file",
      "arguments": {
        "filepath": "test.txt",
        "content": "Hello, MCP Server!"
      }
    }
  }'
```

範例 - 列出檔案：
```bash
curl -X POST http://localhost:8000/file_handler \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "list_files",
      "arguments": {
        "directory": "."
      }
    }
  }'
```

### 管理端點

#### POST /admin/register
動態註冊新的 endpoint (尚未實作)

#### DELETE /admin/unregister/{endpoint_path}
移除已註冊的 endpoint

範例：
```bash
curl -X DELETE http://localhost:8000/admin/unregister/file_handler
```

## 專案結構

```
n8n_mcp_server/
├── app.py                      # 主程式
├── init_db.py                  # 資料庫初始化腳本
├── requirements.txt            # 依賴套件
├── README.md                   # 規格文件
├── USAGE.md                    # 使用指南 (本文件)
├── server/
│   ├── __init__.py
│   └── manager.py             # Endpoint 管理器
├── services/
│   ├── __init__.py
│   └── database.py            # 資料庫服務
└── endpoints/
    ├── __init__.py
    ├── base.py                # Endpoint 基礎類別
    ├── database_ops.py        # 資料庫操作 endpoint
    └── file_handler.py        # 檔案處理 endpoint
```

## 擴展自訂 Endpoint

### 1. 創建新的 Endpoint 檔案

在 `endpoints/` 目錄下創建新檔案，例如 `my_endpoint.py`：

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

### 2. 在 app.py 中註冊

在 `app.py` 的 `startup_event` 函數中加入：

```python
from endpoints.my_endpoint import MyEndpoint

@app.on_event("startup")
async def startup_event():
    # ... 其他程式碼 ...
    
    # 註冊自訂 endpoint
    my_endpoint = MyEndpoint()
    if manager.register_endpoint(my_endpoint):
        print(f"Registered endpoint: {my_endpoint.path}")
```

## 注意事項

1. **資料庫連接**: 預設使用 SQLite (`app.db`)，可以根據需求修改為其他資料庫
2. **安全性**: 目前未實作認證機制，生產環境請加入適當的安全措施
3. **錯誤處理**: 已實作基本錯誤處理，可根據需求增強
4. **FastMCP 整合**: 目前 `handle_mcp_request` 函數使用簡化版實作，需根據實際 FastMCP 2.0 API 調整

## 開發建議

- 使用 `--reload` 模式開發，程式碼變更會自動重啟
- 可以使用 Postman 或類似工具測試 API
- 建議加入日誌記錄以便除錯
- 考慮使用環境變數管理配置

## 故障排除

### 模組找不到錯誤
確保在專案根目錄執行，並且已安裝所有依賴：
```bash
pip install -r requirements.txt
```

### 資料庫連接錯誤
執行 `init_db.py` 初始化資料庫，或檢查 `app.db` 檔案權限

### Port 已被佔用
修改 `app.py` 中的 port 參數，或使用：
```bash
uvicorn app:app --port 8001
```

## 授權

本專案僅供學習和開發參考使用。

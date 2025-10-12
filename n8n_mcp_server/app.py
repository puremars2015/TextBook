"""Multi-Endpoint MCP Server main application"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from server.manager import EndpointManager
from endpoints.database_ops import DatabaseOpsEndpoint
from endpoints.file_handler import FileHandlerEndpoint
from services.database import DatabaseService
import uvicorn
import json

# 初始化
app = FastAPI(title="Multi-Endpoint MCP Server")
manager = EndpointManager()

# 初始化共享服務
db_service = DatabaseService()


@app.on_event("startup")
async def startup_event():
    """伺服器啟動時註冊所有 endpoint"""
    
    # 連接資料庫
    try:
        db_service.connect("app.db")
        print("Database connected")
    except Exception as e:
        print(f"Database connection error: {e}")
    
    # 註冊 database operations endpoint
    db_endpoint = DatabaseOpsEndpoint()
    if manager.register_endpoint(db_endpoint):
        print(f"Registered endpoint: {db_endpoint.path}")
    
    # 註冊 file handler endpoint
    file_endpoint = FileHandlerEndpoint()
    if manager.register_endpoint(file_endpoint):
        print(f"Registered endpoint: {file_endpoint.path}")
    
    print("\nRegistered endpoints:")
    for path, desc in manager.list_endpoints().items():
        print(f"  {path}: {desc}")


@app.on_event("shutdown")
async def shutdown_event():
    """伺服器關閉時清理資源"""
    db_service.close()
    print("Server shutdown, resources cleaned up")


@app.post("/{endpoint_path:path}")
async def handle_mcp_request(endpoint_path: str, request: Request):
    """處理 MCP 請求
    
    Args:
        endpoint_path: endpoint 路徑
        request: FastAPI Request 物件
        
    Returns:
        JSONResponse with MCP protocol data
    """
    # 正規化路徑
    if not endpoint_path.startswith('/'):
        endpoint_path = '/' + endpoint_path
    
    # 取得對應的 MCP server
    mcp_server = manager.get_endpoint(endpoint_path)
    
    if mcp_server is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Endpoint not found: {endpoint_path}"}
        )
    
    try:
        # 取得請求 body
        body = await request.json()
        
        # 使用 FastMCP 處理請求 (根據實際 FastMCP API 調整)
        # 這裡簡化處理,實際需要根據 FastMCP 2.0 的 API 來實作
        response = {
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "result": {
                "message": "MCP request processed",
                "endpoint": endpoint_path
            }
        }
        
        return JSONResponse(content=response)
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "jsonrpc": "2.0",
                "id": body.get("id") if 'body' in locals() else None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
        )


@app.get("/")
async def root():
    """Root endpoint - 服務資訊"""
    return {
        "service": "Multi-Endpoint MCP Server",
        "version": "1.0.0",
        "endpoints": list(manager.list_endpoints().keys())
    }


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
        return JSONResponse(
            status_code=404,
            content={"error": f"Endpoint not found: {endpoint_path}"}
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

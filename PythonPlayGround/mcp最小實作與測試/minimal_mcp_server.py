import datetime
from fastmcp import FastMCP
from starlette.responses import JSONResponse
from starlette.routing import Route

mcp = FastMCP("TestMCP")

# 定義 openapi.yaml 端點的處理函數
async def openapi_manifest(request):
    manifest_data = {
        "schema_version": "v1",
        "name_for_human": "Text Editor",
        "name_for_model": "texteditor",
        "description_for_human": "讀寫文字檔、查詢台北時間及我的最愛歌手。",
        "description_for_model": "這個插件提供四個動作：1) get_tpe_datetime：回傳目前台北時區的日期與時間；2) my_favorite_singer：回傳開發者喜歡的歌手名稱；3) read_txt：讀取指定文字檔並回傳檔案內容；4) write_txt：建立或覆寫指定文字檔並寫入提供的內容。當使用者要求讀取或寫入文字檔、查詢台北時間、或詢問我的最愛歌手時，請調用相應端點。",
        "auth": {
            "type": "none"
        },
        "api": {
            "type": "openapi",
            "url": "https://721f82de6dbfngrok-free.app/openapi.yaml"
        },
        "logo_url": "https://721f82de6dbfngrok-free.app/logo.png",
        "contact_email": "you@example.com",
        "legal_info_url": "https://721f82de6dbfngrok-free.app/legal"
    }
    return JSONResponse(content=manifest_data)


#tool提供AI可執行的操作或功能，AI可以呼叫來完成某些任務
@mcp.tool() 
def get_tpe_datetime() :  
    now = datetime.datetime.now()    #取得本地日期和時間
    return "台北日期時間:"+now.strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool()
def my_Favorite_singer():
    return("我最喜歡的歌手：周杰倫")
 
@mcp.tool()
def read_txt(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"讀取失败: {str(e)}"

@mcp.tool()
def write_txt(filepath: str, content: str, mode: str = 'w'):
    try:
        with open(filepath, mode, encoding="utf-8") as f:
            f.write(content)
        return f"寫入成功: {filepath}"
    except Exception as e:
        return f"寫入失敗: {str(e)}"

if __name__ == '__main__':
    # 在啟動伺服器前,取得底層的 Starlette app 並新增路由
    import uvicorn
    
    # 建立 Starlette app 並新增自訂路由
    app = mcp.streamable_http_app()
    # app.add_route("/openapi.yaml", openapi_manifest, methods=["GET"])
    
    # 啟動伺服器
    uvicorn.run(app, host="127.0.0.1", port=8000)
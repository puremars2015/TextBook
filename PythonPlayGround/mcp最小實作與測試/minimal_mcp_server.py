import datetime
from fastmcp import FastMCP

mcp = FastMCP("TestMCP")


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
    mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")
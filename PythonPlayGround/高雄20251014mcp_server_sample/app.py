from fastmcp import FastMCP
import os
from pathlib import Path

# 建立 MCP server
mcp = FastMCP("文字檔管理服務")

# 設定檔案操作的基礎目錄（可根據需求調整）
BASE_DIR = Path("./text_files")
BASE_DIR.mkdir(exist_ok=True)


def get_safe_path(filename: str) -> Path:
    """確保檔案路徑安全，防止路徑遍歷攻擊"""
    file_path = BASE_DIR / filename
    # 確保路徑在 BASE_DIR 內
    if not str(file_path.resolve()).startswith(str(BASE_DIR.resolve())):
        raise ValueError("不允許存取基礎目錄以外的檔案")
    return file_path


@mcp.tool()
def create_text_file(filename: str, content: str) -> str:
    """
    寫入並產生新文字檔
    
    Args:
        filename: 檔案名稱（例如：test.txt）
        content: 要寫入的文字內容
    
    Returns:
        操作結果訊息
    """
    try:
        file_path = get_safe_path(filename)
        
        # 檢查檔案是否已存在
        if file_path.exists():
            return f"錯誤：檔案 '{filename}' 已存在，請使用編輯功能或選擇其他檔名"
        
        # 建立檔案並寫入內容
        file_path.write_text(content, encoding='utf-8')
        return f"成功建立檔案 '{filename}'，共寫入 {len(content)} 個字元"
    
    except Exception as e:
        return f"建立檔案失敗：{str(e)}"


@mcp.tool()
def edit_text_file(filename: str, content: str, mode: str = "overwrite") -> str:
    """
    編輯指定的文字檔
    
    Args:
        filename: 要編輯的檔案名稱
        content: 新的文字內容
        mode: 編輯模式，'overwrite'（覆寫）或 'append'（附加）
    
    Returns:
        操作結果訊息
    """
    try:
        file_path = get_safe_path(filename)
        
        # 檢查檔案是否存在
        if not file_path.exists():
            return f"錯誤：檔案 '{filename}' 不存在"
        
        # 根據模式進行編輯
        if mode == "overwrite":
            file_path.write_text(content, encoding='utf-8')
            return f"成功覆寫檔案 '{filename}'，共寫入 {len(content)} 個字元"
        elif mode == "append":
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(content)
            return f"成功附加內容到檔案 '{filename}'，附加了 {len(content)} 個字元"
        else:
            return f"錯誤：不支援的編輯模式 '{mode}'，請使用 'overwrite' 或 'append'"
    
    except Exception as e:
        return f"編輯檔案失敗：{str(e)}"


@mcp.tool()
def delete_text_file(filename: str) -> str:
    """
    刪除指定的文字檔
    
    Args:
        filename: 要刪除的檔案名稱
    
    Returns:
        操作結果訊息
    """
    try:
        file_path = get_safe_path(filename)
        
        # 檢查檔案是否存在
        if not file_path.exists():
            return f"錯誤：檔案 '{filename}' 不存在"
        
        # 刪除檔案
        file_path.unlink()
        return f"成功刪除檔案 '{filename}'"
    
    except Exception as e:
        return f"刪除檔案失敗：{str(e)}"


@mcp.tool()
def list_text_files() -> str:
    """
    列出所有文字檔
    
    Returns:
        所有文字檔的列表
    """
    try:
        files = [f.name for f in BASE_DIR.iterdir() if f.is_file()]
        if not files:
            return "目前沒有任何檔案"
        return f"共有 {len(files)} 個檔案：\n" + "\n".join(f"- {f}" for f in sorted(files))
    except Exception as e:
        return f"列出檔案失敗：{str(e)}"


@mcp.tool()
def read_text_file(filename: str) -> str:
    """
    讀取指定文字檔的內容
    
    Args:
        filename: 要讀取的檔案名稱
    
    Returns:
        檔案內容
    """
    try:
        file_path = get_safe_path(filename)
        
        if not file_path.exists():
            return f"錯誤：檔案 '{filename}' 不存在"
        
        content = file_path.read_text(encoding='utf-8')
        return f"檔案 '{filename}' 的內容：\n\n{content}"
    except Exception as e:
        return f"讀取檔案失敗：{str(e)}"


if __name__ == "__main__":
    # 使用 HTTP Streamable 協定啟動 MCP server
    mcp.run(transport="http", host="127.0.0.1", port=8000)
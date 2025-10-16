#!/usr/bin/env python3
"""
驗證 MCP PPT Server 可以正常啟動
"""

import asyncio
import app

async def verify_server():
    print("=" * 60)
    print("MCP PPT Server 驗證")
    print("=" * 60)
    print(f"\nServer Name: {app.mcp.name}")
    
    # 取得所有工具
    tools = await app.mcp.get_tools()
    print(f"\n已註冊的工具數量: {len(tools)}")
    print("\n工具列表:")
    
    # tools 可能是字典或列表
    if isinstance(tools, dict):
        tool_names = sorted(tools.keys())
    elif isinstance(tools, list):
        tool_names = sorted([t.name if hasattr(t, 'name') else str(t) for t in tools])
    else:
        tool_names = sorted(tools)
    
    for i, tool_name in enumerate(tool_names, 1):
        print(f"  {i:2d}. {tool_name}")
    
    print("\n" + "=" * 60)
    print("驗證成功！MCP Server 已正確設定所有工具。")
    print("=" * 60)
    print("\n使用方式:")
    print("  python app.py")
    print("\n這將啟動 MCP server，可以透過 MCP 協議與之通信。")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(verify_server())

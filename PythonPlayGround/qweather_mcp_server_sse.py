import time
import json
import base64
import httpx  #uv add httpx
import asyncio
import jwt  #uv add Pyjwt
from typing import Any
from mcp.server.fastmcp import FastMCP  #uv add mcp

# 初始化 FastMCP
#mcp = FastMCP("weather")
mcp = FastMCP(
    name="weather",
    host="0.0.0.0",
    port=8000,
    description="通過城市名稱取得 實時天氣 或 天氣預報 資訊",
    sse_path="/sse"
)

# 和風天氣 API 設定
QWEATHER_LOCATION_URL = "https://geoapi.qweather.com/v2/city/lookup"        # 查城市 ID
QWEATHER_WEATHER_URL = "https://devapi.qweather.com/v7/weather/now"         # 查即時天氣
QWEATHER_FORECAST_30D_URL = "https://devapi.qweather.com/v7/weather/30d"    # 查 30 天預報
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"

# Set Key ID、Project ID、private key path
KID = "your_credentials_ID," # your credentials ID, JWT Header的 credentials ID 代表使用哪一把公鑰驗證簽名
SUB = "your_project_ID " # your project ID ,JWT Payload的 project ID 代表使用者或專案的唯一識別碼
PRIVATE_KEY_PATH ="/your_private_key_path/ed25519-private.pem"  # 指向私鑰（.pem）的檔案路徑，用來進行簽名

# 🔐 建立 JWT Token
def get_jwt_token() -> str:
    with open(PRIVATE_KEY_PATH, "rb") as f:
        private_key = f.read()

    headers = {"alg": "EdDSA", "kid": KID}
    payload = {
        "sub": SUB,
        "iat": int(time.time()) - 30,
        "exp": int(time.time()) + 900
    }
    return jwt.encode(payload, private_key, algorithm="EdDSA", headers=headers)

# 🔍 查詢城市名稱 → LocationID
async def get_location_id(city: str) -> str | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Authorization": f"Bearer {get_jwt_token()}",
    }
    params = {"location": city}
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(QWEATHER_LOCATION_URL, headers=headers, params=params)
            res.raise_for_status()
            data = res.json()
            if data.get("code") == "200" and data.get("location"):
                return data["location"][0]["id"]
        except Exception as e:
            print(f"查詢地點錯誤: {e}")
    return None

# ☁️ 查即時天氣
async def get_weather_from_location_id(location_id: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Authorization": f"Bearer {get_jwt_token()}",
    }
    params = {"location": location_id}
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(QWEATHER_WEATHER_URL, headers=headers, params=params)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(f"查詢天氣錯誤: {e}")
    return None

# 🌤 查30天天氣預報
async def get_forecast_30d(location_id: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Authorization": f"Bearer {get_jwt_token()}",
    }
    params = {"location": location_id}
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(QWEATHER_FORECAST_30D_URL, headers=headers, params=params)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(f"查詢預報錯誤: {e}")
    return None

# ✨ 格式化即時天氣資訊
def format_weather(data: dict[str, Any]) -> str:
    if not data or data.get("code") != "200":
        return f"查詢失敗，錯誤代碼: {data.get('code', '未知')}"
    now = data.get("now", {})
    return (
        f"【即時天氣】\n"
        f"狀態: {now.get('text', '未知')}\n"
        f"溫度: {now.get('temp', '未知')}°C\n"
        f"濕度: {now.get('humidity', '未知')}%\n"
        f"風速: {now.get('windSpeed', '未知')} km/h"
    )

# 🌦 格式化 30 天預報資訊（只顯示前 3 天摘要）
def format_forecast(data: dict[str, Any]) -> str:
    if not data or data.get("code") != "200":
        return f"查詢預報失敗，錯誤代碼: {data.get('code', '未知')}"
    
    days = data.get("daily", [])[:3]  # 顯示前3天
    result = ["【未來三天天氣預報】"]
    for d in days:
        result.append(
            f"{d.get('fxDate', '未知日期')} 🌡️ {d.get('tempMin', '?')}~{d.get('tempMax', '?')}°C ☀️ {d.get('textDay', '?')} / 🌙 {d.get('textNight', '?')}"
        )
    return "\n".join(result)

# ✅ MCP 工具 1：即時天氣查詢
@mcp.tool()
async def get_weather_from_cityname_tool(city: str) -> str:
    location_id = await get_location_id(city)
    if not location_id:
        return f"找不到城市「{city}」，請確認拼音或城市名稱是否正確。"
    data = await get_weather_from_location_id(location_id)
    return format_weather(data)

# ✅ MCP 工具 2：30 天預報查詢
@mcp.tool()
async def get_forecast_30d_tool(city: str) -> str:
    """
    根據城市名稱查詢未來 30 天天氣預報（僅顯示前三天）
    """
    location_id = await get_location_id(city)
    if not location_id:
        return f"找不到城市「{city}」，請確認拼音或城市名稱是否正確。"
    data = await get_forecast_30d(location_id)
    return format_forecast(data)

# 🚀 啟動 MCP
if __name__ == "__main__":
    #mcp.run(transport='stdio')
    print("Starting server...")
    mcp.run(transport='sse')
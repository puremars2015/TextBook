# Vibe Coding 技巧教學2 (以 Python 網站為例)

本篇教你用「Vibe Coding」的方式（用 AI 輔助寫程式，但用規格與驗收把品質拉回來），在 **Windows + VS Code + Python** 環境做出一個能跑、能驗收、可迭代的小型 Python 網站。

> 這篇不是「叫 AI 生一坨程式碼」；而是教你把 AI 變成可控的工程產線：每次只改一小步、每次都有驗收條件、每次都能回滾。

---

## 你會完成什麼（可驗收成果）

完成後，你應該能做到：

1. 在本機建立一個乾淨的 Python 虛擬環境（venv）
2. 用 Flask 建立一個最小網站：
	 - `GET /` 回傳一個 HTML 頁面
	 - `GET /api/hello?name=Sean` 回傳 JSON
3. 用「規格 + 驗收」驅動 AI 修改程式，而不是盲改
4. 碰到錯誤時，能用 traceback 把 AI 拉回正軌：定位根因 → 最小修補 → 重新驗收

---

## 適用對象與前置假設

- 你會基本命令列操作（PowerShell 或 CMD）
- 你會安裝 Python、能在 VS Code 開資料夾
- 你想做的是「能跑的網站」：先求跑得起來，再談架構與部署

本篇預設：

- OS：Windows
- Editor：VS Code
- Python：3.10+（建議 3.11/3.12 也可）

---

## Vibe Coding 的核心觀念（一句話）

**先寫規格（spec）與驗收（acceptance criteria），再叫 AI 產出最小可跑版本，最後用小步迭代把品質補回來。**

你要把 AI 當成「很快的實習生」，而不是「自動交付系統」：

- 你提供：需求、限制、檔案結構、驗收條件
- AI 產出：候選實作
- 你負責：驗收、把錯誤訊息給 AI、控制改動範圍

---

## Vibe Coding 標準流程（建議照順序跑）

### Step 0：先讓 AI 問你問題（避免亂猜）

如果你直接說「幫我做一個網站」，AI 會自己腦補一堆東西。
你要先讓它問你 2–5 個澄清問題，再開始寫。

### Step 1：寫清楚「規格」

規格至少包含：

- 功能（要做什麼）
- 範圍（不做什麼）
- 介面（路由、輸入、輸出、錯誤）
- 限制（Windows、不要 Docker、只能 Flask…）

### Step 2：寫清楚「驗收條件」

驗收條件是「能用命令/瀏覽器測出來」的句子，例如：

- 開啟 `http://127.0.0.1:5000/` 會看到標題 `Vibe Coding Demo`
- `GET /api/hello?name=Amy` 回 `{"message":"Hello, Amy"}`（HTTP 200）

### Step 3：請 AI 只產出「最小可跑版本」

最小版本的原則：

- 只做必要功能
- 先不做登入、資料庫、背景任務
- 先不引入一堆套件

### Step 4：跑起來 → 驗收 → 紀錄問題

不要靠「看程式碼覺得可以」；要跑、要測。

### Step 5：小步迭代（每次只改一件事）

每次迭代都要：

1. 說明你要改什麼
2. 說明不改什麼
3. 說明驗收方式
4. 要求 AI **只改動少數檔案**

---

## Prompt 模板庫（可直接複製）

你可以把下面這些模板存成 VS Code 的 snippet 或常用筆記。

### 模板 A：先問我澄清問題

```text
你要幫我做一個 Python 網站功能。
在開始寫任何程式碼前，請先問我 3 個你必須知道的澄清問題（只問問題，不要先寫解法）。
```

### 模板 B：規格 → 驗收 → 檔案樹 → 產出

```text
請依照以下規格完成專案。

【規格】
- 技術：Python + Flask
- OS：Windows
- 需求：
	1) GET / 回傳一個簡單 HTML 頁面
	2) GET /api/hello?name=xxx 回傳 JSON: {"message": "Hello, xxx"}
- 不做：資料庫、登入、Docker

【驗收條件】
- 用瀏覽器打開 / 看得到標題文字
- 用 curl 打 /api/hello?name=Amy 得到 HTTP 200 與正確 JSON

【輸出格式】
1) 先給我檔案結構（tree）
2) 再給每個檔案的完整內容
3) 最後給我 Windows PowerShell 的建立 venv、安裝、啟動指令
```

### 模板 C：限制改動範圍（避免 AI 大改）

```text
請在不改動既有行為的前提下，完成以下修改。
限制：
- 只允許修改這 2 個檔案：<檔名1>、<檔名2>
- 不要新增新的外部套件
- 如果你覺得一定要新增檔案/套件，先停下來提出理由與替代方案
```

### 模板 D：我貼錯誤，請你用「根因→最小修補→驗收」

```text
我遇到錯誤，請你依序輸出：
1) 根因判斷（引用 traceback 的關鍵行）
2) 最小修補方案（改哪些檔案、改哪些行）
3) 我該怎麼驗收（給我 2~3 個命令或操作）

【環境】Windows + VS Code
【我做了什麼】<步驟>
【錯誤全文】
<貼上完整 traceback>
```

### 模板 E：請你幫我寫「測試/驗收」而不是只寫功能

```text
請不要直接加功能；請先幫我補上最小的驗收方式（例如 curl 命令或簡單 pytest），
再依照驗收去完成實作。
```

---

## 實作：Flask 最小網站（從 0 到能跑）

下面用最小步驟做一個「能跑、能驗收」的 Flask 服務。

### 1) 建資料夾

在你要放專案的地方建立資料夾，例如：

```powershell
mkdir vibe-flask-demo
cd vibe-flask-demo
```

### 2) 建立並啟動 venv

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

如果你遇到 PowerShell 執行政策（ExecutionPolicy）阻擋，先用替代做法：

- 方案 1：改用 CMD 啟動

```bat
.venv\Scripts\activate.bat
```

- 方案 2：只對目前 PowerShell 視窗放行（較安全）

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### 3) 安裝 Flask

```powershell
py -m pip install -U pip
py -m pip install Flask
```

### 4) 建立 `app.py`

建立檔案 `app.py`，內容如下：

```python
from __future__ import annotations

from flask import Flask, jsonify, request


def create_app() -> Flask:
		app = Flask(__name__)

		@app.get("/")
		def index():
				return """<!doctype html>
<html lang=\"zh-Hant\">
	<head>
		<meta charset=\"utf-8\" />
		<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
		<title>Vibe Coding Demo</title>
	</head>
	<body>
		<h1>Vibe Coding Demo</h1>
		<p>如果你看到這頁，代表 Flask 已經跑起來了。</p>
		<p>試試看：<a href=\"/api/hello?name=Sean\">/api/hello?name=Sean</a></p>
	</body>
</html>"""

		@app.get("/api/hello")
		def hello_api():
				name = (request.args.get("name") or "World").strip()
				if not name:
						return jsonify({"error": "name is required"}), 400
				return jsonify({"message": f"Hello, {name}"})

		return app


if __name__ == "__main__":
		app = create_app()
		app.run(host="127.0.0.1", port=5000, debug=True)
```

> 為什麼不用 80 port？
> 在 Windows 上用 80 常會碰到權限/占用問題；教學建議先用 5000，少踩雷。

### 5) 啟動

```powershell
py app.py
```

看到類似以下輸出就代表成功：

```text
Running on http://127.0.0.1:5000
```

### 6) 驗收

用瀏覽器打開：

- `http://127.0.0.1:5000/`

再用 PowerShell 測 API（用 curl）：

```powershell
curl "http://127.0.0.1:5000/api/hello?name=Amy"
```

預期回應（JSON 類似）：

```json
{"message":"Hello, Amy"}
```

### 7) Vibe Coding 迭代示範：加一個健康檢查端點

**需求：** 加 `GET /healthz` 回 `{"ok": true}`。

**你要給 AI 的提示：**

```text
請在現有 Flask app 加上一個 GET /healthz 端點，回傳 JSON {"ok": true}。
限制：只改 app.py，不要新增套件，不要改既有 / 與 /api/hello 行為。
驗收：curl http://127.0.0.1:5000/healthz 應回 200 與 {"ok":true}
```

---

## 除錯：用 traceback 驅動 AI 修正（最有效的 Vibe 技巧）

### 原則：你要貼「完整錯誤」而不是一句話

你給 AI 的資料越完整，它越不需要腦補。

最少要貼：

1. 你做了什麼（幾步就好）
2. 你預期看到什麼
3. **完整 traceback**（從第一行到最後一行）

### 常見錯誤範例 1：ModuleNotFoundError

如果你看到：

```text
ModuleNotFoundError: No module named 'flask'
```

通常代表：

- 你沒有啟動 venv
- 或你在別的 Python 環境安裝到 Flask

**最小修正流程：**

```powershell
.venv\Scripts\Activate.ps1
py -m pip install Flask
py app.py
```

### 常見錯誤範例 2：Address already in use（port 被占用）

看到類似：

```text
OSError: [WinError 10048] Only one usage of each socket address...
```

**最小修正：**

- 改 port：把 `port=5000` 改成 `port=5001`
- 或找出占用的程式，再關掉

（你也可以把錯誤全文貼給 AI，叫它教你查占用與修正）

---

## 小步重構：讓專案更可維護（但不要一開始就做）

當你已經「跑得起來」後，再把程式整理成更可維護的形式。

建議的最小重構目標：

- 用 `create_app()` 工廠模式（上面示範已經做了）
- 把設定從程式碼抽成環境變數（例如 PORT）
- 加上基本 logging（至少能看 request/錯誤）

你可以用這個 prompt 叫 AI 幫你做最小重構：

```text
請幫我把目前的 Flask 程式做最小重構：
1) 保持現有路由與輸出完全不變
2) 允許用環境變數 PORT 改 port，預設 5000
3) 加上 basic logging（啟動時印出啟動資訊）
限制：不要新增新套件；如果一定要新增，先提出理由
請先列出你要改哪些行，再給我完整 app.py
```

---

## 部署入門（擇一）：先知道選項與最低限度注意事項

> 這章不追求「一次就上線」，目標是讓你知道：部署不是把 debug 模式打開就好。

### 選項 1：IIS（Windows 原生）

- 適合：公司內網、Windows Server、希望用 IIS 管理
- 關鍵點：要用 WSGI（例如 `wfastcgi` 或其他方式），並處理權限與應用程式池設定

若你要走 IIS 路線，可參考同教材中的 IIS/Flask 教學文件（IIS 設定細節很多，建議獨立一篇處理）。

### 選項 2：Docker + nginx（跨平台常見做法）

- 適合：要可攜、要跟環境隔離、要 reverse proxy
- 關鍵點：Flask 開發伺服器不適合 production；production 常用 gunicorn/uwsgi + nginx

如果你已經在專案裡有 Docker/nginx 範例，也可以照那個結構去套。

---

## 常見坑速查（Windows 最常踩）

1. **PowerShell 啟動 venv 被擋**：用 `Set-ExecutionPolicy -Scope Process Bypass` 或改用 `activate.bat`
2. **port 80/443**：容易需要管理員權限或被別的服務占用；教學先用 5000/8000
3. **安裝到錯的 Python**：統一用 `py -m pip ...`，避免 pip 指到別的環境
4. **Debug 模式**：只用在本機開發，部署不要用 `debug=True`
5. **亂改一大堆**：每次只改一件事；要求 AI 限制修改檔案數量

---

## 練習題（照 Vibe 流程做：規格→驗收→改→驗收）

### 練習 1：增加回應格式

需求：`/api/hello` 多回 `{"time": "<ISO時間>"}`。

驗收：呼叫兩次回應時間不同，且仍有 `message`。

### 練習 2：增加輸入驗證

需求：`name` 長度 > 30 時回 `400`，JSON 包含 `error`。

驗收：

- `name=Amy` → 200
- `name=` → 400
- `name=<超長字串>` → 400

### 練習 3：加一個 `/api/echo`（GET）

需求：`GET /api/echo?text=hi` 回 `{"text":"hi"}`。

限制：不要改動既有端點行為。

---

## 一頁命令速查

```powershell
# 建 venv
py -m venv .venv

# 啟動 venv（PowerShell）
.\ .venv\Scripts\Activate.ps1

# 更新 pip
py -m pip install -U pip

# 安裝套件
py -m pip install Flask

# 跑起來
py app.py
```
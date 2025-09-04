# AutoGenStudio安裝流程.md

## 前置條件
0. 確定你用的是windows, 如果是mac, 請對應修正
1. 安裝好Python
3. 確定powershell可以叫出python跟pip指令, 如不行, 請補設定環境變數(方法請ai告訴你)
4. 找個風水寶地,喔不是,是一個空的檔案夾,然後啟動powershell,並確認路徑在該檔案夾


## 安裝步驟
1. 安裝uv工具
```
pip install uv
```

2. 建立python虛擬環境
```
uv venv
```

3. 初始化專案
```
uv init --bare
```

4. 安裝 AutoGen
```
uv add autogen-agentchat~=0.2
```

5. 安裝 AutoGen Studio（GUI 工具）
```
uv add autogenstudio
```

6. 同步依賴並準備虛擬環境
```
uv sync
```

7. 啟動 AutoGen Studio
```
uv run autogenstudio ui --port 8081
```

執行成功後，可透過瀏覽器存取：http://localhost:8081/，進入 AutoGen Studio 的工作界面。

其他特殊設定：
--host <address>：指定可讓遠端存取的介面，例如 0.0.0.0
--appdir <路徑>：變更預設資料儲存位置（預設 ~/.autogenstudio）
--database-uri <URI>：設定資料庫位置（如 SQLite 或 PostgreSQL）
--reload：開啟程式變更即時重載功能（開發用）

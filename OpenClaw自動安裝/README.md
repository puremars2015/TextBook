# OpenClaw自動安裝程式 for Windows

## 介紹
OpenClaw自動安裝程式是一個用於簡化OpenClaw安裝過程的工具。它提供了一個簡單的界面，讓用戶可以輕鬆地安裝和配置OpenClaw，無需手動處理複雜的安裝步驟。

並提供對應的操作控制板，讓用戶可以方便地管理和控制OpenClaw的運行狀態。

## 功能
- 軟體以python的gui套件tkinter開發，提供一個簡單易用的界面。
- 自動檢查、下載和安裝OpenClaw所需的依賴項。
    - powershell有沒有更新到7.x版?
    - 包括Python、Node.js、Git等必要工具。
    - PowerShell腳本將自動處理這些安裝過程，確保用戶無需手動干預。
- 提供一個簡單的界面，讓用戶可以輕鬆地安裝和配置OpenClaw。
- 提供對應的操作控制板，讓用戶可以方便地啟動、停止和監控OpenClaw的運行狀態。
- 提供啟動dashboard的功能，讓用戶可以不用透過命令行就能啟動dashboard。
- 提供反安裝openclaw的功能，讓用戶可以方便地卸載openclaw。

## 已實作內容
- `openclaw_manager.py`：以 `tkinter` 開發的 Windows GUI 工具。
- `scripts/openclaw_helper.ps1`：負責檢查環境、安裝依賴、安裝/反安裝 OpenClaw、停止 Gateway。
- `run_openclaw_manager.ps1`：Windows 啟動器，會自動用 `py -3` 或 `python` 啟動 GUI。

## 工具功能
- 檢查 PowerShell 7、Node.js、npm、Git、Python、OpenClaw 是否已安裝。
- 使用 `winget` 自動安裝或更新 PowerShell 7、Node.js LTS、Git、Python 3.12。
- 使用 `npm install -g openclaw@latest` 安裝 OpenClaw。
- 使用 `npm uninstall -g openclaw` 反安裝 OpenClaw。
- 以 GUI 啟動 `openclaw onboard --install-daemon`。
- 以 GUI 啟動與停止 `openclaw gateway --port 18789 --verbose`。
- 直接開啟本機 Dashboard：`http://127.0.0.1:18789`。
- 提供 `openclaw doctor` 按鈕做快速診斷。

## 執行方式
1. 先確認本機已安裝 Python 3。
2. 在 PowerShell 執行：

```powershell
.\run_openclaw_manager.ps1
```

3. 進入 GUI 後，建議依序操作：
    - `重新檢查`
    - `安裝/更新依賴`
    - `安裝 OpenClaw`
    - `啟動 Onboard`
    - `啟動 Gateway`
    - `開啟 Dashboard`

## 打包成單一 EXE
在專案根目錄執行：

```powershell
.\build_single_exe.ps1
```

完成後會產生單一執行檔：

```text
.\dist\OpenClawManager.exe
```

說明：
- 此打包方式使用 PyInstaller `--onefile`。
- `scripts/openclaw_helper.ps1` 會被一起打包進 EXE，執行時自動解壓到暫存目錄。
- 打包後使用者只需要拿到 `OpenClawManager.exe` 即可執行，不需要另外攜帶 `.ps1` 或 `.py` 檔案。

## 注意事項
- 依賴安裝使用 `winget`，若系統沒有 `winget`，需要先補安裝 App Installer。
- OpenClaw 官方 README 建議 Windows 使用 WSL2；本工具先提供原生 Windows 安裝與操作流程。
- 若剛安裝完 Node.js 或 OpenClaw，GUI 內部會重新檢查 npm 全域路徑，避免 PATH 尚未刷新時找不到 `openclaw`。

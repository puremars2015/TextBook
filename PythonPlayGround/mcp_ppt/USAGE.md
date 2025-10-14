# MCP PPT Server 使用指南

## 已實作功能

根據 README.md 規格，本 MCP Server 實作了以下 8 個工具：

### 1. set_template
設定樣板簡報，並回傳可用版面配置
- 輸入：樣板 .pptx 檔案路徑
- 輸出：樣板資訊與可用版面配置列表

### 2. create_presentation
建立工作中的簡報物件
- 輸入：是否使用樣板、metadata（標題、作者、日期）
- 輸出：session_id（用於後續操作）

### 3. add_slide
以結構化資料新增單張投影片
- 輸入：session_id、版面配置、標題、副標題、項目符號、圖片、備註
- 輸出：投影片索引

### 4. compile_from_description
解析「文字敘述 DSL」，批次建立簡報
- 輸入：DSL 文字、樣板路徑（可選）、素材資料夾路徑
- 輸出：session_id、投影片數量、警告訊息

### 5. list_layouts
列出目前樣板或工作中的簡報可用版面
- 輸入：無
- 輸出：版面配置列表

### 6. insert_image
在指定投影片插圖
- 輸入：session_id、投影片索引、圖片路徑、位置與尺寸（可選）
- 輸出：成功/失敗狀態

### 7. finalize_and_save
儲存並結束工作階段
- 輸入：session_id、輸出資料夾、檔案名稱
- 輸出：檔案絕對路徑、檔案大小

### 8. reset
釋放所有工作階段與樣板快取
- 輸入：無
- 輸出：成功/失敗狀態

## 啟動 Server

```bash
# 啟動 MCP server（streamable HTTP 模式，預設）
python app.py

# 啟動在指定 port（預設 8000）
python app.py http 8080

# 啟動在 stdio 模式
python app.py stdio

# 啟動在 SSE 模式
python app.py sse 8080
```

預設啟動方式為 **streamable HTTP** 模式，監聽在 `0.0.0.0:8000`。

## DSL 語法範例

```
# 簡報標題: 產品介紹
# 作者: John Doe
# 日期: 2025-01-13

[Slide]
layout: 0
title: 歡迎
subtitle: 產品介紹簡報

[Slide]
layout: Title and Content
title: 產品特色
bullets:
- 功能強大
- 易於使用
- 價格合理
notes: 強調性價比

[Slide]
layout: 1
title: 技術架構
bullets:
- 前端：React
- 後端：Python
- 資料庫：PostgreSQL
```

## 工作流程範例

1. **使用樣板（可選）**
   ```
   set_template("path/to/template.pptx")
   ```

2. **建立簡報**
   ```
   create_presentation(use_template=true, metadata={...})
   ```

3. **新增投影片（兩種方式）**
   - 方式 A：逐張新增
     ```
     add_slide(session_id, layout=0, title="標題", bullets=[...])
     ```
   - 方式 B：使用 DSL 批次建立
     ```
     compile_from_description(description_text="...")
     ```

4. **儲存簡報**
   ```
   finalize_and_save(session_id, filename="output.pptx")
   ```

## 檔案結構

```
mcp_ppt/
├── app.py                 # MCP Server 主程式
├── requirements.txt       # Python 套件依賴
├── README.md             # 規格文件
├── USAGE.md              # 本使用指南
└── output/               # 輸出資料夾（自動建立）
    ├── *.pptx           # 生成的簡報檔案
    └── mcp_ppt.log      # 日誌檔案
```

## 錯誤處理

所有工具在失敗時會回傳統一的錯誤格式：

```json
{
  "ok": false,
  "error_code": "ERROR_CODE",
  "message": "錯誤訊息",
  "detail": "詳細資訊（可選）"
}
```

錯誤代碼包括：
- `TEMPLATE_NOT_FOUND`: 找不到樣板檔案
- `INVALID_LAYOUT`: 無效的版面配置
- `FILE_IO_ERROR`: 檔案讀寫錯誤
- `PARSE_ERROR`: DSL 解析錯誤
- `SESSION_NOT_FOUND`: 找不到工作階段
- `IMAGE_NOT_FOUND`: 找不到圖片檔案
- `PPTX_WRITE_ERROR`: 簡報寫入錯誤
- `UNSUPPORTED`: 不支援的操作

## 注意事項

1. 最多同時支援 8 個工作階段（可在 app.py 調整 MAX_SESSIONS）
2. 所有檔案路徑會自動轉換為絕對路徑
3. 圖片路徑找不到時會略過並產生警告
4. 版面配置名稱不存在時會使用預設版面並產生警告
5. 日誌檔案位於 `./output/mcp_ppt.log`

## 驗證安裝

執行以下指令驗證 server 正常運作：

```bash
python verify_server.py
```

應該會顯示 8 個已註冊的工具。

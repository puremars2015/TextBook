# MCP Server 規格（FastMCP + python-pptx，僅本機，單檔 `app.py`）

## 目標

* 依「文字敘述」生成新的 PowerPoint（`.pptx`）。
* 可指定「既有簡報檔」作為樣板，沿用其版面配置與字體色票。
* 輸出為本機檔案路徑，回傳給 Host。
* 以多個可獨立呼叫的 MCP 工具提供操作。

## 非目標

* 不做雲端儲存、遠端下載、CORS。
* 不做 LLM 摘要或高階版面規劃推理。Host LLM 應先將需求轉為本規格之輸入格式。

## 執行環境

* Python 3.10+
* 套件：`fastmcp`, `python-pptx`, `pydantic`
* 平台：本機（localhost）。單檔 `app.py`。
* 檔案系統：可讀取樣板 `.pptx`、可讀寫輸出資料夾與素材檔。

## 檔案與路徑約定

* 預設輸出資料夾：`./output/`（自動建立）。
* 預設素材資料夾：呼叫時由參數傳入，或使用相對路徑。
* 回傳一律為標準化的絕對路徑字串。

## 資料模型

### A. 文字敘述語法（供 `compile_from_description` 使用）

* UTF-8 純文字。以段落定義投影片。支援最小 DSL：

```
# 簡報標題: {title?}
# 作者: {author?}
# 日期: {date?}

[Slide]
layout: {layout_name 或 layout_index}
title: {文字}
subtitle: {文字?}
bullets:
- {項目}
- {項目}
image: {相對或絕對路徑?}
notes: {講者備註?}

[Slide]
layout: Title and Content
title: 產品路線圖
bullets:
- Q1: 完成 POC
- Q2: 小規模上線
```

* `layout` 可用樣板中的「版面配置名稱」或整數索引。
* 欄位可省略；未填則用版面預設或留白。

### B. 結構化投影片描述（供細粒度工具）

```json
{
  "slides": [
    {
      "layout": "Title and Content",
      "title": "願景",
      "subtitle": null,
      "bullets": ["提高良率", "縮短交期"],
      "image": null,
      "notes": "強調 KPI"
    }
  ],
  "metadata": {
    "author": "Sean",
    "date": "2025-10-13",
    "title": "年度簡報"
  }
}
```

## 工具一覽（MCP Tools）

> 名稱以蛇形命名；每個工具以 JSON Schema 定義 `input` 與 `output`。錯誤以統一錯誤模型回傳。

### 1) `set_template`

設定樣板簡報，並回傳可用版面配置。

* **input**

```json
{
  "template_path": "string"  // 現有 .pptx 路徑
}
```

* **output**

```json
{
  "ok": true,
  "template_abs_path": "string",
  "layouts": [
    {"index": 0, "name": "Title Slide"},
    {"index": 1, "name": "Title and Content"}
  ],
  "theme": {
    "color_scheme_names": ["Accent1","Accent2"],
    "font_families": ["..."]  // 可選，若可擷取
  }
}
```

### 2) `create_presentation`

建立工作中的簡報物件（以目前樣板或空白）。

* **input**

```json
{
  "use_template": true,
  "metadata": {
    "title": "string?",
    "author": "string?",
    "date": "string?"   // ISO 或自由字串
  }
}
```

* **output**

```json
{"ok": true, "session_id": "string"}  // 用於後續追加
```

### 3) `add_slide`

以結構化資料新增單張投影片。

* **input**

```json
{
  "session_id": "string",
  "layout": "Title and Content",      // 或整數索引
  "title": "string?",
  "subtitle": "string?",
  "bullets": ["string", "..."]?,
  "image": "string?",                 // 檔案路徑（選填）
  "notes": "string?"
}
```

* **output**

```json
{"ok": true, "index": 5}
```

### 4) `compile_from_description`

解析「文字敘述 DSL」，批次建立簡報。

* **input**

```json
{
  "template_path": "string?",         // 未設定時用既有樣板或空白
  "description_text": "string",       // 依上方 DSL
  "assets_base_dir": "string?"        // 解析 image 相對路徑用
}
```

* **output**

```json
{
  "ok": true,
  "session_id": "string",
  "slide_count": 12,
  "warnings": ["string", "..."]       // 例如找不到版面名時的回退資訊
}
```

### 5) `list_layouts`

列出目前樣板或工作中的簡報可用版面。

* **input**

```json
{}
```

* **output**

```json
{"ok": true, "layouts": [{"index":0,"name":"Title Slide"}, {"index":1,"name":"Title and Content"}]}
```

### 6) `insert_image`

在指定投影片插圖，支援定位與自動縮放。

* **input**

```json
{
  "session_id": "string",
  "slide_index": 3,
  "image_path": "string",
  "left": "float?",     // 英吋，可選
  "top": "float?",
  "width": "float?",    // 三者用任兩者即可，未填則自動縮放置中
  "height": "float?"
}
```

* **output**

```json
{"ok": true}
```

### 7) `finalize_and_save`

儲存並結束工作階段。

* **input**

```json
{
  "session_id": "string",
  "output_dir": "string?",     // 預設 ./output
  "filename": "string?"        // 預設自動命名
}
```

* **output**

```json
{
  "ok": true,
  "pptx_abs_path": "string",
  "size_bytes": 123456
}
```

### 8) `reset`

釋放所有工作階段與樣板快取。

* **input**: `{}`
* **output**: `{"ok": true}`

## 錯誤模型（統一）

所有工具失敗時以下列結構回傳，HTTP 200，`ok=false`。

```json
{
  "ok": false,
  "error_code": "TEMPLATE_NOT_FOUND | INVALID_LAYOUT | FILE_IO_ERROR | PARSE_ERROR | SESSION_NOT_FOUND | IMAGE_NOT_FOUND | PPTX_WRITE_ERROR | UNSUPPORTED",
  "message": "string",
  "detail": "string?"
}
```

## 工作流程範例（Host 側邏輯）

1. 呼叫 `set_template` 指定 `template_path`，取得 `layouts`。
2. 呼叫 `create_presentation`（可附 `metadata`）。
   3a. 細粒度路徑：多次呼叫 `add_slide`、`insert_image`。
   3b. 一次性路徑：呼叫 `compile_from_description` 並檢查 `warnings`。
3. 呼叫 `finalize_and_save`，取得 `pptx_abs_path`。

## 驗證與回退策略

* `layout`：先以名稱嚴格比對；失敗時嘗試以索引；仍失敗則回退第一個內容版面並加入 `warnings`。
* 文字長度：超長將自動縮放字級或換行；無法滿足則截斷並加入 `warnings`。
* 圖片：找不到路徑則忽略該圖並加入 `warnings`。
* 樣板未設定時：以空白簡報建立並 `warnings` 提示。

## 相容性與限制（python-pptx）

* 不支援直接讀寫母片的全部樣式細節；色票與字型多仰賴樣板套用。
* 不原生支援智慧圖或圖表生成；需後續擴充工具再加入（可預留 `insert_chart` 未來版）。

## 效能與並發

* 以 `session_id` 區分同時作業。單機以記憶體保存工作中的 `Presentation`。
* 預設最大並行工作階段 `MAX_SESSIONS=8`（可在程式常數調整）。超限回 `UNSUPPORTED`。

## 日誌

* 層級：INFO（主要流程）、WARN（回退）、ERROR（例外）。
* 檔案：`./output/mcp_ppt.log`。

## 安全

* 僅存取呼叫中提供之路徑。禁止相對路徑跳脫到根目錄以外的白名單外位置（可選擇性啟用簡單沙箱：限制在專案根下）。
* 無 CORS。無外部網路請求。

## 測試要點（黑箱）

* 無樣板、有效樣板、錯誤版面名。
* 圖片存在與不存在、尺寸自動與手動。
* 文字敘述 DSL 的極端情況：缺欄位、空段、混合索引與名稱。
* 多工作階段並行建立與釋放。

## 設定常數（在 `app.py` 頂部）

* `OUTPUT_DIR = "./output"`
* `MAX_SESSIONS = 8`
* `DEFAULT_FILENAME_FMT = "ppt_{timestamp}.pptx"`

## Host 端提示（關鍵）

* 你提供「文字敘述」時，請先由 LLM 轉成本規格 DSL 或直接使用 `compile_from_description`。
* 若需要精準控制布局與元素位置，請改用細粒度工具組合（`add_slide`、`insert_image`）。

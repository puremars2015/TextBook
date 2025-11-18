# 使用指南

## 安裝步驟

1. **安裝 Python 套件**
```bash
pip install -r requirements.txt
```

2. **安裝 Playwright 瀏覽器**
```bash
playwright install chromium
```

3. **（可選）安裝並啟動 MongoDB**
```bash
# macOS 使用 Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community

# 或使用 Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

## 執行爬蟲

```bash
python app.py
```

## 程式說明

### 主要功能

1. **自動搜尋判決書**
   - 使用 Playwright 自動化瀏覽器
   - 搜尋關鍵字：「詐騙」（可自訂）

2. **資料解析**
   - 使用 BeautifulSoup 解析 HTML
   - 提取案號、日期、案由、法院等資訊

3. **資料儲存**
   - 優先儲存到 MongoDB
   - 備份儲存到 JSON 檔案（`judgments.json`）

### 自訂參數

在 `app.py` 的 `main()` 函數中可以修改：

```python
crawler = JudgmentCrawler(
    keyword="詐騙",  # 修改搜尋關鍵字
    mongodb_uri="mongodb://localhost:27017/"  # 修改 MongoDB 連接字串
)
```

### 重要提醒

1. **網站選擇器需調整**
   - 司法院網站的實際 HTML 結構可能不同
   - 需要檢查網站並調整以下方法中的選擇器：
     - `search_judgments()`: 搜尋框和按鈕的選擇器
     - `parse_judgment_list()`: 判決書列表的選擇器

2. **查看實際網站結構**
   - 執行程式時設定 `headless=False` 可以看到瀏覽器操作過程
   - 發生錯誤時會自動截圖（`error_screenshot.png`）

3. **調整爬取數量**
   - 目前限制只爬取前 10 筆資料（在 `parse_judgment_list()` 中的 `[:10]`）
   - 可依需求調整

## 除錯步驟

1. **檢查網站結構**
   - 打開瀏覽器開發者工具
   - 檢查搜尋框、按鈕、結果列表的實際選擇器

2. **調整選擇器**
   - 根據實際網站結構修改 CSS 選擇器
   - 測試是否能正確抓取元素

3. **查看錯誤截圖**
   - 程式會在發生錯誤時保存 `error_screenshot.png`
   - 可以檢視當時的頁面狀態

## 進階功能（待實作）

- [ ] 整合 LangChain 進行 AI 分析
- [ ] 爬取判決書全文內容
- [ ] 批次爬取多頁結果
- [ ] 加入代理伺服器支援
- [ ] 實作重試機制
- [ ] 資料清洗與正規化

## 注意事項

- 請遵守網站的 robots.txt 和使用條款
- 避免過於頻繁的請求，建議加入適當的延遲
- 此程式僅供學習研究使用

# AI爬蟲研究

以https://judgment.judicial.gov.tw/FJUD/default.aspx為範例

## 目標

1. 爬取判決書資料
2. 分析判決書內容
3. 建立判決書資料庫

## 技術棧

- Python
- LangChain + Playwright
- BeautifulSoup
- MongoDB

## 實作步驟

0. 設定要查詢的案例關鍵字:詐騙
1. 使用LangChain + Playwright建立爬蟲
2. 設定爬取規則
3. 解析HTML內容
4. 儲存資料到MongoDB

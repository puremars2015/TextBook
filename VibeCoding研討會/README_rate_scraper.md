# BOT 匯率爬蟲說明

此腳本會從 https://rate.bot.com.tw/xrt?Lang=zh-TW 抓取台幣對各國匯率，並輸出為 Excel 檔案。

快速開始：

1. 建議在虛擬環境中安裝相依套件：

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

2. 執行爬蟲並輸出 Excel（預設輸出 `rates.xlsx`）：

```bash
python rate_bot_scraper.py -o rates.xlsx
```

3. 產生的檔案會包含原始表格欄位加上一欄 `ScrapedAt` 記錄抓取時間。

注意：網站版面若改變，解析規則可能需要調整。

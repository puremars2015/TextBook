# Taifex 交易資料下載程式使用說明

這個程式可以從臺灣期貨交易所 (TAIFEX) 下載特定日期的交易資料。

## 安裝依賴

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 下載今天的資料

```bash
python app.py
```

### 2. 下載特定日期的資料

使用 YYYY-MM-DD 格式：
```bash
python app.py 2024-01-15
```

或使用 YYYY/MM/DD 格式：
```bash
python app.py 2024/01/15
```

## 功能說明

- 自動建立 `data` 目錄儲存下載的檔案
- 支援多種日期格式 (YYYY-MM-DD 或 YYYY/MM/DD)
- 包含完整的錯誤處理和使用者回饋
- 自動檢查檔案大小，避免下載空檔案
- 顯示下載進度和結果

## 輸出檔案

下載的檔案會儲存在 `data` 目錄中，檔案名稱格式為：
```
taifex_trading_data_YYYYMMDD.csv
```

例如：`taifex_trading_data_20240115.csv`

## 注意事項

- 需要網路連線才能下載資料
- 確保指定的日期是交易日，非交易日可能無資料
- 資料來源：https://www.taifex.com.tw/cht/3/dlFutPrevious30DaysSalesData

## 程式結構

- `download_taifex_data(date, save_dir)`: 核心下載函數
  - `date`: 日期參數（可選，預設為今天）
  - `save_dir`: 儲存目錄（預設為 'data'）
  - 返回值：成功返回 True，失敗返回 False

- `main()`: 主程式入口，處理命令列參數

## 範例

```python
from app import download_taifex_data

# 下載特定日期的資料
download_taifex_data('2024-01-15')

# 下載到指定目錄
download_taifex_data('2024-01-15', save_dir='my_data')
```

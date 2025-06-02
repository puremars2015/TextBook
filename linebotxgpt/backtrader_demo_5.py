import yfinance as yf
import mplfinance as mpf

# 下載台指期資料
ticker = 'FITX'  # 台指期的 Yahoo 財經代號
data = yf.download(ticker, start='2024-08-01', end='2024-08-31')

# 檢查資料是否成功下載
if data.empty:
    print("無法下載台指期資料。請檢查代號或日期範圍。")
else:
    # 繪製 K 線圖
    mpf.plot(data, type='candle', style='charles', title='台指期 日線圖', volume=True)

import backtrader as bt
import yfinance as yf


# 定義 MACD 策略
class MACDStrategy(bt.Strategy):
    params = (
        ('macd1', 12),  # 短期均線
        ('macd2', 26),  # 長期均線
        ('signal', 9),  # 信號線 (基於 MACD 計算)
    )

    def __init__(self):
        # 初始化 MACD 指標
        self.macd = bt.indicators.MACD(
            self.data.close,
            period_me1=self.params.macd1,
            period_me2=self.params.macd2,
            period_signal=self.params.signal
        )

        # 定義 MACD 的交叉信號
        self.crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

        # 初始化訂單變量
        self.order = None

    def next(self):
        # 當 MACD 線上穿信號線時，生成買入信號
        if self.crossover > 0:
            if not self.position:
                self.order = self.buy(size=1)
                # print(f"BUY at {self.data.datetime.date(0)} price: {self.data.close[0]}")

        # 當 MACD 線下穿信號線時，生成賣出信號
        elif self.crossover < 0:
            if self.position:
                self.order = self.sell(size=1)
                # print(f"SELL at {self.data.datetime.date(0)} price: {self.data.close[0]}")

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                print(f"BUY EXECUTED at {order.executed.price}")
            elif order.issell():
                print(f"SELL EXECUTED at {order.executed.price}")

            # 打印當前持倉數量
            print(f"Current Position Size: {self.position.size}")
            # 打印當前資金總值
            print(f"Current Portfolio Value: {self.broker.getvalue()}")

        # 清除訂單狀態
        self.order = None

# 創建回測環境

# 自定義 Feed 來整合 yfinance 資料
class YahooFinanceData(bt.feeds.PandasData):
    params = (('datetime', None),
              ('open', 'Open'),
              ('high', 'High'),
              ('low', 'Low'),
              ('close', 'Close'),
              ('volume', 'Volume'),
              ('openinterest', None))

# 下載數據
data = yf.download('^IXIC', start='2024-01-01', end='2024-11-06')

# 將數據保存到 CSV 檔案
data.to_csv('twii_data.csv')

# 將數據轉換成 backtrader 可以使用的格式
data_feed = YahooFinanceData(dataname=data)

# 設置 backtrader
cerebro = bt.Cerebro()
cerebro.adddata(data_feed)

# 這裡添加策略、設置資金等
cerebro.addstrategy(MACDStrategy)

# 設定初始資金
cerebro.broker.setcash(5000)

# 設置槓桿和保證金
cerebro.broker.setcommission(leverage=4)  # 槓桿 10 倍，保證金 20%，手續費 1%

# 執行回測
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())


# 繪製結果
cerebro.plot()
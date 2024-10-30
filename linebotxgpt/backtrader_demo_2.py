import backtrader as bt
import yfinance as yf
import matplotlib.pyplot as plt  # 匯入 matplotlib

# 定義 MACD 策略
class MACDStrategy(bt.Strategy):

    xt = 0

    params = (
        ('macd1', 12),  # 短期均線
        ('macd2', 26),  # 長期均線
        ('signal', 9),  # 信號線 (基於 MACD 計算)
    )

    def __init__(self):
        self.macd = bt.indicators.MACD(
            self.data.close,
            period_me1=self.params.macd1,
            period_me2=self.params.macd2,
            period_signal=self.params.signal
        )
        self.crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)
        self.order = None
        self.trade_dates = []  # 紀錄每次交易的日期與價格

    def next(self):
        self.xt += 1
        trade_date = self.data.datetime.date(0)
        print(f"xt: {self.xt} {trade_date}")
        if self.crossover > 0:
            if not self.position:
                self.order = self.buy(size=1)
                self.trade_dates.append((trade_date, self.data.close[0], 'BUY'))

        elif self.crossover < 0:
            if self.position:
                self.order = self.sell(size=1)
                self.trade_dates.append((trade_date, self.data.close[0], 'SELL'))

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                print(f"BUY EXECUTED at {order.executed.price} on {self.data.datetime.date(0)}")
            elif order.issell():
                print(f"SELL EXECUTED at {order.executed.price} on {self.data.datetime.date(0)}")
            print(f"Current Position Size: {self.position.size}")
            print(f"Current Portfolio Value: {self.broker.getvalue()}")

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
data = yf.download('^TWII', start='2024-01-01', end='2024-10-01')
data_feed = YahooFinanceData(dataname=data)

# 設置 backtrader
cerebro = bt.Cerebro()
cerebro.adddata(data_feed)
cerebro.addstrategy(MACDStrategy)
cerebro.broker.setcash(5000)
cerebro.broker.setcommission(leverage=5, margin=0.2, commission=1)

# 執行回測
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
strategies = cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# 繪製回測結果
fig = cerebro.plot(iplot=False)[0][0]

# 顯示每次交易的符號和日期
strategy = strategies[0]
for trade_date, price, action in strategy.trade_dates:
    plt.text(trade_date, price, f'{action}\n{trade_date}', 
             fontsize=8, ha='center', va='bottom', 
             bbox=dict(facecolor='white', alpha=0.7))

# 調整日期格式
fig.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
fig.autofmt_xdate()  # 自動調整日期標籤的角度

plt.show()

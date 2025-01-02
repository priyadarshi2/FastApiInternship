from src.indicators.common_indicators import CustomTALibIndicator
import backtrader as bt

class CustomTALibStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),           # RSI and Bollinger Bands
        ('fastperiod', 12),           # MACD fast period
        ('slowperiod', 26),           # MACD slow period
        ('signalperiod', 9),          # MACD signal line
        ('timeperiod', 18),           # SMA, EMA, OBV EMA
        ('nbdevup', 2),               # Bollinger Bands upper deviation
        ('nbdevdn', 2),               # Bollinger Bands lower deviation
        ('matype', 0),                # Moving average type for Bollinger Bands
        ('rsi_overbought', 70),       # RSI overbought threshold
        ('rsi_oversold', 30)
    )

    def __init__(self, key_list):
        # Add the custom TA-Lib indicator with the parameters
        self.custom_ind = CustomTALibIndicator(
            self.data,
            period=self.params.rsi_period,
            fastperiod=self.params.fastperiod,
            slowperiod=self.params.slowperiod,
            signalperiod=self.params.signalperiod,
            timeperiod=self.params.timeperiod,
            nbdevup=self.params.nbdevup,
            nbdevdn=self.params.nbdevdn,
            matype=self.params.matype
        )

        self.key_list = key_list
        self.trades = []  # Initialize a list to store trades
        self.starting_cash = None 
        self.ending_cash = None        
        self.profit = None
        self.profit_perc = None
        self.keys = [False, False , False, False, False]
        
    def selections(self):
        for i in self.key_list:
            self.keys[i] = True

    def next(self):
        # Extract individual lines from the custom indicator
        rsi = self.custom_ind.rsi[0] if self.keys[0] else None
        sma = self.custom_ind.sma[0] if self.keys[4] else None
        ema = self.custom_ind.ema[0] if self.keys[4] else None
        macd = self.custom_ind.macd[0] if self.keys[1] else None
        macdsignal = self.custom_ind.macdsignal[0] if self.keys[1] else None
        macdhist = self.custom_ind.macdhist[0] if self.keys[1] else None
        upperband = self.custom_ind.upperband[0] if self.keys[2] else None
        middleband = self.custom_ind.middleband[0] if self.keys[2] else None
        lowerband = self.custom_ind.lowerband[0] if self.keys[2] else None
        obv = self.custom_ind.obv[0] if self.keys[3] else None
        obv_ema = self.custom_ind.obv_ema[0] if self.keys[3] else None
        close = self.data.close[0]
        self.selections()

         # Buy condition: We need at least one indicator to be valid
        if not self.position:
            buy_signal = False

            # Check each indicator if it is enabled
            if self.keys[0] and rsi is not None and rsi < self.params.rsi_oversold:
                buy_signal = True
            if self.keys[2] and lowerband is not None and close < lowerband:
                buy_signal = True
            if self.keys[1] and macd is not None and macd > macdsignal:
                buy_signal = True
            if self.keys[4] and sma is not None and close > sma:
                buy_signal = True
            if self.keys[4] and ema is not None and close > ema:
                buy_signal = True
            if self.keys[3] and obv is not None and obv > 0:  # Just a simple example for OBV
                buy_signal = True

            if buy_signal:
                self.buy()
                print(f"Buy Signal: Close={close}, RSI={rsi}, MACD={macd}, SMA={sma}, EMA={ema}, OBV={obv}")
                self.trades.append({
                    'action': 'buy',
                    'price': self.data.close[0],
                    'datetime': self.data.datetime.datetime(0)
                })

        # Sell condition: Check if any indicator is giving a signal
        elif self.position:
            sell_signal = False

            # Check each indicator if it is enabled
            if self.keys[0] and rsi is not None and rsi > self.params.rsi_overbought:
                sell_signal = True
            if self.keys[2] and upperband is not None and close > upperband:
                sell_signal = True
            if self.keys[1] and macd is not None and macd < macdsignal:
                sell_signal = True
            if self.keys[4] and sma is not None and close < sma:
                sell_signal = True
            if self.keys[4] and ema is not None and close < ema:
                sell_signal = True
            if self.keys[3] and obv is not None and obv < 0:  # Just a simple example for OBV
                sell_signal = True

            if sell_signal:
                self.close()
                print(f"Sell Signal: Close={close}, RSI={rsi}, MACD={macd}, SMA={sma}, EMA={ema}, OBV={obv}")
                self.trades.append({
                    'action': 'sell',
                    'price': self.data.close[0],
                    'datetime': self.data.datetime.datetime(0)
                })

    def stop(self):
        # Store ending cash value
        self.starting_cash = round(self.broker.startingcash,3)
        print("=========starting_cash cash==================",self.starting_cash)
        self.ending_cash = round(self.broker.getcash(),3)
        print("=========ending cash==================",self.ending_cash)
        self.profit = round((self.ending_cash - self.starting_cash),3)
        print("==========profit==============",self.profit)
        self.profit_perc = round((self.profit/self.starting_cash) * 100, 3)
        print("==============profit%=================", self.profit_perc)

strats = {
            '1' : "rsi",
            '2' : "macd",
            '3' : "bollinger",
            '4' : "obv",
            '5' : "sma_ema"
        }

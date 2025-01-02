from src.indicators.common_indicators import CustomTALibIndicator
import backtrader as bt

class CommonTALibStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),           # RSI and Bollinger Bands
        ('fastperiod', 12),           # MACD fast period
        ('slowperiod', 26),           # MACD slow period
        ('signalperiod', 9),          # MACD signal line
        ('timeperiod', 18),           # SMA, EMA, OBV EMA
        ('nbdevup', 2),               # Bollinger Bands upper deviation
        ('nbdevdn', 2),               # Bollinger Bands lower deviation
        ('matype', 0)                 # Moving average type for Bollinger Bands
    )

    def __init__(self):
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
        self.trades = []  # Initialize a list to store trades
        self.starting_cash = None 
        self.ending_cash = None        
        self.profit = None
        self.profit_perc = None

    def next(self):
        # Extract individual lines from the custom indicator
        rsi = self.custom_ind.rsi[0]
        sma = self.custom_ind.sma[0]
        ema = self.custom_ind.ema[0]
        macd = self.custom_ind.macd[0]
        macdsignal = self.custom_ind.macdsignal[0]
        macdhist = self.custom_ind.macdhist[0]
        upperband = self.custom_ind.upperband[0]
        middleband = self.custom_ind.middleband[0]
        lowerband = self.custom_ind.lowerband[0]
        obv = self.custom_ind.obv[0]
        obv_ema = self.custom_ind.obv_ema[0]

        
        # Print indicator values for debugging
        print(f"RSI: {rsi}, Close: {self.data.close[0]}, LowerBand: {lowerband}, UpperBand: {upperband}")

        # Buy condition: RSI below 30 and close below the lower Bollinger Band
        if not self.position:  # If no position is open
            if rsi < 30 and self.data.close[0] < lowerband:
                self.buy()
                print(f"Buy executed - RSI: {rsi}, Close: {self.data.close[0]}, LowerBand: {lowerband}")
                # Log the trade details
                self.trades.append({
                    'action': 'buy',
                    'price': self.data.close[0],
                    'datetime': self.data.datetime.datetime(0)
                })

        # Sell condition: RSI above 70 and close above the upper Bollinger Band
        elif self.position:  # If a position is open
            if rsi > 70 and self.data.close[0] > upperband:
                self.close()
                print(f"Sell executed - RSI: {rsi}, Close: {self.data.close[0]}, UpperBand: {upperband}")
                # Log the trade details
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

class RSI_BAND_Strategy(bt.Strategy):
    params = (
        ('rsi_period', 14),           # RSI and Bollinger Bands
        ('fastperiod', 12),           # MACD fast period
        ('slowperiod', 26),           # MACD slow period
        ('signalperiod', 9),          # MACD signal line
        ('timeperiod', 18),           # SMA, EMA, OBV EMA
        ('nbdevup', 2),               # Bollinger Bands upper deviation
        ('nbdevdn', 2),               # Bollinger Bands lower deviation
        ('matype', 0)                 # Moving average type for Bollinger Bands
    )

    def __init__(self):
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
        self.trades = []  # Initialize a list to store trades
        self.starting_cash = None 
        self.ending_cash = None        
        self.profit = None
        self.profit_perc = None

    def next(self):
        # Extract individual lines from the custom indicator
        rsi = self.custom_ind.rsi[0]
        sma = self.custom_ind.sma[0]
        ema = self.custom_ind.ema[0]
        macd = self.custom_ind.macd[0]
        macdsignal = self.custom_ind.macdsignal[0]
        macdhist = self.custom_ind.macdhist[0]
        upperband = self.custom_ind.upperband[0]
        middleband = self.custom_ind.middleband[0]
        lowerband = self.custom_ind.lowerband[0]
        obv = self.custom_ind.obv[0]
        obv_ema = self.custom_ind.obv_ema[0]

        
        # Print indicator values for debugging
        #print(f"RSI: {rsi}, Close: {self.data.close[0]}, LowerBand: {lowerband}, UpperBand: {upperband}")

        # Buy condition: RSI below 30 and close below the lower Bollinger Band
        if not self.position:  # If no position is open
            if rsi < 30 and self.data.close[0] < lowerband:
                self.buy()
                print(f"Buy executed - RSI: {rsi}, Close: {self.data.close[0]}, LowerBand: {lowerband}")
                # Log the trade details
                self.trades.append({
                    'action': 'buy',
                    'price': self.data.close[0],
                    'datetime': self.data.datetime.datetime(0)
                })

        # Sell condition: RSI above 70 and close above the upper Bollinger Band
        elif self.position:  # If a position is open
            if rsi > 70 and self.data.close[0] > upperband:
                self.close()
                print(f"Sell executed - RSI: {rsi}, Close: {self.data.close[0]}, UpperBand: {upperband}")
                # Log the trade details
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

class MACDStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),           # RSI and Bollinger Bands
        ('fastperiod', 12),           # MACD fast period
        ('slowperiod', 26),           # MACD slow period
        ('signalperiod', 9),          # MACD signal line
        ('timeperiod', 18),           # SMA, EMA, OBV EMA
        ('nbdevup', 2),               # Bollinger Bands upper deviation
        ('nbdevdn', 2),               # Bollinger Bands lower deviation
        ('matype', 0)                 # Moving average type for Bollinger Bands
    )

    def __init__(self):
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
        self.trades = []  # Initialize a list to store trades
        self.starting_cash = None 
        self.ending_cash = None        
        self.profit = None
        self.profit_perc = None

    def next(self):
        # Extract individual lines from the custom indicator
        rsi = self.custom_ind.rsi[0]
        sma = self.custom_ind.sma[0]
        ema = self.custom_ind.ema[0]
        macd = self.custom_ind.macd[0]
        macdsignal = self.custom_ind.macdsignal[0]
        macdhist = self.custom_ind.macdhist[0]
        upperband = self.custom_ind.upperband[0]
        middleband = self.custom_ind.middleband[0]
        lowerband = self.custom_ind.lowerband[0]
        obv = self.custom_ind.obv[0]
        obv_ema = self.custom_ind.obv_ema[0]

        # Buy condition: MACD crosses above the Signal Line
        if not self.position:  # If no position is open
            if macd > macdsignal:  # Bullish crossover
                self.buy()
                print(f"Buy executed - MACD: {macd}, MACD Signal: {macdsignal}")
                # Log the trade details
                self.trades.append({
                    'action': 'buy',
                    'price': self.data.close[0],
                    'datetime': self.data.datetime.datetime(0)
                })

        # Sell condition: MACD crosses below the Signal Line
        elif self.position:  # If a position is open
            if macd < macdsignal:  # Bearish crossover
                self.close()
                print(f"Sell executed - MACD: {macd}, MACD Signal: {macdsignal}")
                # Log the trade details
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

class OBVStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),           # RSI and Bollinger Bands
        ('fastperiod', 12),           # MACD fast period
        ('slowperiod', 26),           # MACD slow period
        ('signalperiod', 9),          # MACD signal line
        ('timeperiod', 18),           # SMA, EMA, OBV EMA
        ('nbdevup', 2),               # Bollinger Bands upper deviation
        ('nbdevdn', 2),               # Bollinger Bands lower deviation
        ('matype', 0)                 # Moving average type for Bollinger Bands
    )

    def __init__(self):
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
        self.trades = []  # Initialize a list to store trades
        self.starting_cash = None 
        self.ending_cash = None        
        self.profit = None
        self.profit_perc = None

    def next(self):
        # Extract individual lines from the custom indicator
        rsi = self.custom_ind.rsi[0]
        sma = self.custom_ind.sma[0]
        ema = self.custom_ind.ema[0]
        macd = self.custom_ind.macd[0]
        macdsignal = self.custom_ind.macdsignal[0]
        macdhist = self.custom_ind.macdhist[0]
        upperband = self.custom_ind.upperband[0]
        middleband = self.custom_ind.middleband[0]
        lowerband = self.custom_ind.lowerband[0]
        obv = self.custom_ind.obv[0]
        obv_ema = self.custom_ind.obv_ema[0]

        # Buy condition: OBV crosses above its EMA
        if not self.position:  # If no position is open
            if obv > obv_ema:
                self.buy()
                print(f"Buy executed - OBV: {obv}, OBV EMA: {obv_ema}")
                # Log the trade details
                self.trades.append({
                    'action': 'buy',
                    'price': self.data.close[0],
                    'datetime': self.data.datetime.datetime(0)
                })

        # Sell condition: OBV crosses below its EMA
        elif self.position:  # If a position is open
            if obv < obv_ema:
                self.close()
                print(f"Sell executed - OBV: {obv}, OBV EMA: {obv_ema}")
                # Log the trade details
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

Strategy_Key = {
    1 : RSI_BAND_Strategy,
    2 : MACDStrategy,
    3 : OBVStrategy,
}
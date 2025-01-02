import backtrader as bt 
import talib 
import numpy as np


class CustomTALibIndicator(bt.Indicator):
    lines = ('rsi', 'sma', 'ema', 'macd', 'macdsignal', 'macdhist',
             'upperband', 'middleband', 'lowerband', 'obv', 'obv_ema')

    params = (
        ('period', 14),           # RSI and Bollinger Bands
        ('fastperiod', 12),       # MACD fast period
        ('slowperiod', 26),       # MACD slow period
        ('signalperiod', 9),      # MACD signal line
        ('timeperiod', 18),       # SMA, EMA, OBV EMA
        ('nbdevup', 2),           # Bollinger Bands upper deviation
        ('nbdevdn', 2),           # Bollinger Bands lower deviation
        ('matype', 0)             # Moving average type for Bollinger Bands
    )

    def __init__(self):
        # Ensure enough data for all indicators
        self.addminperiod(
            max(
                self.params.period,
                self.params.fastperiod + self.params.slowperiod,
                self.params.timeperiod
            )
        )

    def next(self):
        # Extract data
        close_prices = np.array(self.data.close.get(size=len(self.data)))
        volumes = np.array(self.data.volume.get(size=len(self.data)))

        # Compute RSI
        if len(close_prices) >= self.params.period:
            rsi_values = talib.RSI(close_prices, timeperiod=self.params.period)
            self.lines.rsi[0] = rsi_values[-1]

        # Compute SMA and EMA
        if len(close_prices) >= self.params.timeperiod:
            self.lines.sma[0] = talib.SMA(close_prices, timeperiod=self.params.timeperiod)[-1]
            self.lines.ema[0] = talib.EMA(close_prices, timeperiod=self.params.timeperiod)[-1]

        # Compute MACD
        if len(close_prices) >= self.params.slowperiod:
            macd, macdsignal, macdhist = talib.MACD(
                close_prices,
                fastperiod=self.params.fastperiod,
                slowperiod=self.params.slowperiod,
                signalperiod=self.params.signalperiod
            )
            self.lines.macd[0] = macd[-1]
            self.lines.macdsignal[0] = macdsignal[-1]
            self.lines.macdhist[0] = macdhist[-1]

        # Compute Bollinger Bands
        if len(close_prices) >= self.params.period:
            upperband, middleband, lowerband = talib.BBANDS(
                close_prices,
                timeperiod=self.params.period,
                nbdevup=self.params.nbdevup,
                nbdevdn=self.params.nbdevdn,
                matype=self.params.matype
            )
            self.lines.upperband[0] = upperband[-1]
            self.lines.middleband[0] = middleband[-1]
            self.lines.lowerband[0] = lowerband[-1]

        # Compute OBV and OBV EMA
        if len(close_prices) >= 2:  # OBV requires at least 2 data points
            obv = talib.OBV(close_prices, volumes)
            self.lines.obv[0] = obv[-1]

            if len(obv) >= self.params.timeperiod:
                self.lines.obv_ema[0] = talib.EMA(obv, timeperiod=self.params.timeperiod)[-1]

        # Handle missing data cases
        else:
            self.lines.rsi[0] = float('nan')
            self.lines.sma[0] = float('nan')
            self.lines.ema[0] = float('nan')
            self.lines.macd[0] = float('nan')
            self.lines.macdsignal[0] = float('nan')
            self.lines.macdhist[0] = float('nan')
            self.lines.upperband[0] = float('nan')
            self.lines.middleband[0] = float('nan')
            self.lines.lowerband[0] = float('nan')
            self.lines.obv[0] = float('nan')
            self.lines.obv_ema[0] = float('nan')



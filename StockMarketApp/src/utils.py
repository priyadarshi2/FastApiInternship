import requests
from fastapi import HTTPException
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

import pandas as pd
import numpy as np
import talib as ta
import backtrader as bt 

from src.indicators import CustomTALibStrategy

load_dotenv()

def get_articles(symb : str):
    # Your API Key
    API_KEY = os.getenv("NEWS_API_KEY")

    # News API endpoint for searching articles
    BASE_URL = "https://newsapi.org/v2/everything"

    # Stock symbol or company name to search
    stock_query = symb

    #set the limit of the fetched articles to 5
    article_limit = 5

    # Parameters for the request
    params = {
        "q": stock_query,           # Query term (stock name or symbol)
        "language": "en",           # Language of the news (e.g., 'en' for English)
        "sortBy": "publishedAt",    # Sort results by relevance or publishedAt
        "pageSize" : article_limit, # Set the limit of the articles to be fetched 
        "apiKey": API_KEY,          # Your News API key
    }

    # Make the API request
    response = requests.get(BASE_URL, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        news_data = response.json()
        articles = news_data.get("articles", [])
        return articles
    else:
        print(f"Error: Unable to fetch news (Status Code: {response.status_code})")
    
def fetch_articles(symb : str):
    articles = get_articles(symb)

    if articles:
        texts = ""
        for idx, article in enumerate(articles, start=1):
            article_url = article['url']
            try:
                # Request the article's webpage
                article_response = requests.get(article_url, timeout=10)
                if article_response.status_code == 200:
                    soup = BeautifulSoup(article_response.content, "html.parser")
                    
                    # Extract the main content (refine based on publisher's structure)
                    paragraphs = soup.find_all("p")
                    full_text = " ".join(p.get_text() for p in paragraphs)  
                else:
                    print("   Could not fetch the full article content.")
            except Exception as e:
                raise HTTPException(status_code=404, detail = f'{e}')
        return full_text
    else:
        raise HTTPException(status_code=200, detail="Information not available")
    
# def strategize(data):
 
#     data_closes = []
#     data_volume = []
#     ret_list = []

#     for close, volume in zip(data['Close'], data['Volume']):
#         # Keep track of the closing prices and volumes
#         data_volume.append(volume)
#         data_closes.append(close)
        
#         # Convert the lists to numpy arrays
#         int_data = [float(x) for x in data_volume]
#         np_volume = np.array(int_data)
        
#         float_data = [float(x) for x in data_closes]
#         np_closes = np.array(float_data)
        
#         # Once we have some data to analyze    
#         if len(np_closes) > 20 and len(np_volume) > 20:
            
#             # Calculate RSI (Relative Strength Index)
#             RSI = ta.RSI(np_closes, timeperiod = 14) # Calculate RSI for last 14 closing prices
            
#             # Calculate Moving Averages
#             SMA = ta.SMA(np_closes, timeperiod = 20) # Calculate Simple Moving Average for last 20 closing prices
#             EMA = ta.EMA(np_closes, timeperiod = 20) # Calculate Exponential Moving Average for last 20 closing prices
            
#             # Calculate MACD (Moving Average Convergence Divergence)
#             MACD, MACDsignal, MACDhist = ta.MACD(np_closes, fastperiod=12, slowperiod=26, signalperiod=9)
            
#             # Bollinger Bands
#             upperband, middleband, lowerband = ta.BBANDS(np_closes, timeperiod=18, nbdevup=2, nbdevdn=2, matype=0)
            
#             # OBV
#             OBV = ta.OBV(np_closes, np_volume)
#             OBV_EMA = ta.EMA(OBV, timeperiod=18)

#             ret_list.append([close, volume, RSI[-1], SMA[-1], EMA[-1], MACD[-1], MACDsignal[-1], MACDhist[-1], upperband[-1], middleband[-1], lowerband[-1], OBV[-1], OBV_EMA[-1]])
#             # Display the first few rows of the data with the new technical indicators
#     ta_df = pd.DataFrame(ret_list, columns=['Close', 'Volume', 'RSI', 'SMA', 'EMA', 'MACD', 'MACDsignal', 'MACDhist', 'upperband', 'middleband', 'lowerband', 'OBV', 'OBV_EMA'])
#     ta_df.index = pd.to_datetime(data.index[-len(ta_df):]).tz_localize(None)
#     print(ta_df.head(10))
#     return ta_df

# class TaLibStrategy(bt.Strategy):
#     def __init__(self):
#         self.data_close = self.datas[0].close
#         self.rsi = self.datas[0].lines.rsi
#         self.sma = self.datas[0].lines.sma
#         self.ema = self.datas[0].lines.ema
#         self.macd = self.datas[0].lines.macd
#         self.macdsignal = self.datas[0].lines.macdsignal
#         self.macdhist = self.datas[0].lines.macdhist
#         self.upperband = self.datas[0].lines.upperband
#         self.middleband = self.datas[0].lines.middleband
#         self.lowerband = self.datas[0].lines.lowerband
#         self.obv = self.datas[0].lines.obv
#         self.obv_ema = self.datas[0].lines.obv_ema
#         self.order = None

#         self.trades = []
#         self.starting_cash = None 
#         self.ending_cash = None

#     def next(self):
#         print(f"RSI: {self.rsi[-1]}, Close: {self.data_close[-1]}, LowerBand: {self.lowerband[-1]}, UpperBand: {self.upperband[-1]}")
#         if not self.position:
#             if self.rsi[-1] < 30 and self.data_close[-1] < self.lowerband[-1]:
#                 self.buy()
#                 print(f"self.rsi : {self.rsi[-1]}, data close : {self.data_close[-1]}, upperband : {self.upperband[-1]}")                   
#                 self.trades.append({'action': 'buy', 'price': self.data_close[0], 'datetime': self.data.datetime.datetime(0)})
#         elif self.position:
#             if self.rsi[-1] > 70 and self.data_close[-1] > self.upperband[-1]:
#                 self.close()
#                 print(f"self.rsi : {self.rsi[-1]}, data close : {self.data_close[-1]}, upperband : {self.upperband[-1]}")
#                 self.trades.append({'action': 'sell', 'price': self.data_close[0], 'datetime': self.data.datetime.datetime(0)})
        
#     def stop(self):
#         # Store ending cash value
#         self.starting_cash = self.broker.startingcash
#         print("=========starting_cash cash==================",self.starting_cash)
#         self.ending_cash = self.broker.getcash()
#         print("=========ending cash==================",self.ending_cash)

# class CustomPandasData(bt.feeds.PandasData):
#     lines = ('rsi', 'sma', 'ema', 'macd', 'macdsignal', 'macdhist', 'upperband', 'middleband', 'lowerband', 'obv', 'obv_ema')
    
#     params = (
#         ('datetime',None),
#         ('rsi', -1),
#         ('sma', -1),
#         ('ema', -1),
#         ('macd', -1),
#         ('macdsignal', -1),
#         ('macdhist', -1),
#         ('upperband', -1),
#         ('middleband', -1),
#         ('lowerband', -1),
#         ('obv', -1),
#         ('obv_ema', -1),
#     )


def backtest(data):

    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro = bt.Cerebro()
    cerebro.adddata(data_feed)
    cerebro.addstrategy(CustomTALibStrategy)
    cerebro.broker.set_cash(100000)
    cerebro.broker.setcommission(commission=0.001)
    # Run the backtest
    print("Running the backtest...")

    backtest_result = cerebro.run()
    print("Backtest completed.")
    print(f"Ending Cash: {cerebro.broker.getcash()}")
    strategy = backtest_result[0]
    results = {
        'starting_cash': strategy.starting_cash,
        'ending_cash': strategy.ending_cash,
        'profit': strategy.ending_cash - strategy.starting_cash,
        'trades': strategy.trades
    }
    return results



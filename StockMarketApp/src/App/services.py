import pandas as pd 
import yfinance as yf
from datetime import datetime 

def string_to_time(text  : str):
    return datetime.strptime(text, "%Y-%m-%d")

def get_data(symb: str, start_date : str, end_date : str):
    start_date = string_to_time(start_date)
    end_date = string_to_time(end_date)
    data = yf.download(symb, start=start_date, end=end_date)
    result = data.reset_index()[["Date", "Open", "High", "Low", "Close", "Volume"]].to_dict(orient="records")
    return {"symbol" : symb, "data": result}

def get_daily_change(symb : str, start_date : str, end_date : str):
    start_date = string_to_time(start_date)
    end_date = string_to_time(end_date)
    data = yf.download(symb, start=start_date, end=end_date)
    data["Daily_Change"] = ((data["Close"] - data["Close"].shift(1))/data["Close"].shift(1)) * 100
    result = data.reset_index()[["Date", "Daily_Change"]].dropna().to_dict(orient="records")
    return {"symbol" : symb, "change" : result}

def get_moving_average(symb : str, window_ : int, start_date : str, end_date : str):
    start_date = string_to_time(start_date)
    end_date = string_to_time(end_date)
    data = yf.download(symb, start=start_date, end=end_date)
    data[f"moving_{window_}"] = data["Close"].rolling(window=window_).mean()
    result = data.reset_index()[["Date",f"moving_{window_}"]].dropna().to_dict(orient="records")
    return {"symbol" : symb, "moving_average" : result}
                        



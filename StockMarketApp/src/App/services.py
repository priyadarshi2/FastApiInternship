import pandas as pd 
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from datetime import datetime 
import datetime as dt
from src.utils import fetch_articles
from src.transformer import predict_sentiment
from src.amzn import amzn
from src.googleai import gooogleAI
from src.cache import write_json, load_json, extract_value, search_key

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

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

def create_features(data, window_size):
    x, y = [], []
    for i in range(window_size, len(data)):
        x.append(data[i-window_size:i])
        y.append(data[i])
    return np.array(x), np.array(y)

def create_model(symb : str):
    now = datetime.now(dt.timezone.utc)
    previous = datetime.now(dt.timezone.utc) - relativedelta(years=1)
    data = yf.download(symb, previous, now)
    data = data.dropna()
    prices = data["Close"].values
    window_size = 200  # Use past 200 days' closing prices
    x, y = create_features(prices, window_size)

    # Split the data into train and test sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)

    x_train_flat = x_train.reshape(x_train.shape[0], -1)  # Flatten to 2D
    x_test_flat = x_test.reshape(x_test.shape[0], -1)

    # Scale the features
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train_flat)
    x_test_scaled = scaler.transform(x_test_flat)  
    return x_train_scaled, x_test_scaled, y_train, y_test

def train_model(symb : str):
    x_train_scaled, x_test_scaled, y_train, y_test = create_model(symb) 
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(x_train_scaled, y_train)

    # Make predictions
    predictions = model.predict(x_test_scaled)

    # Evaluate the model
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    print(f'Root Mean Squared Error: {rmse}')
    print("=====================>",predictions)   
    return predictions

def get_prediction(symb : str):
    result = train_model(symb)
    return {"symbol" : symb, "prediction" : result}

def get_news(symb : str):
    news = fetch_articles(symb)
    return {"symbol" : symb, "prediction" : news}

def make_decision(articles):
    positive_count = 0
    negative_count = 0

    for article in articles:
        sentiment = predict_sentiment(article)
        if sentiment == 2:  # Positive sentiment
            positive_count += 1
        elif sentiment == 0:  # Negative sentiment
            negative_count += 1

    # Decision based on aggregate sentiment
    if positive_count > negative_count:
        return "Buy It"
    else:
        return "Don't buy it"
    
def get_verdict(symb : str):
    if search_key(symb):
        result = extract_value(symb)
    else:
        news = fetch_articles(symb)
        result = gooogleAI(symb, news)
        answer = {symb : result}
        write_json(answer)
    return {"symbol" : symb, "toBuy" : result}

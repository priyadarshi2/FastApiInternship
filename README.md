# Stock Analysis App in FastAPI

This is a foundational stock analysis program built using FastAPI. It reads stock data within a specified time range for any given stock and provides analytical insights and opinions based on that data.

## Description

The program supports six GET requests, enabling users to view stock data, daily changes, moving averages for specific windows, relevant news articles, predicted stock prices for the next day, and the program's own recommendations on stock purchases.The program leverages Google's Gemini API to obtain text-based feedback on stocks and utilizes NewsAPI to retrieve relevant articles about the queried stock


## Program Structure
The program uses the following directory structure:\
**StockMarketApp**\
├── src\
│  ├── App\
│  │  ├── __pycache_\_\
│  │  │  ├── routes.cpython-312.pyc\
│  │  │  ├── schema.cpython-312.pyc\
│  │  │  └── services.cpython-312.pyc\
│  │  ├── routes.py\
│  │  ├── schema.py\
│  │  └── services.py\
│  ├── __pycache_\_\
│  │  ├── amzn.cpython-312.pyc\
│  │  ├── cache.cpython-312.pyc\
│  │  ├── googleai.cpython-312.pyc\
│  │  ├── transformer.cpython-312.pyc\
│  │  └── utils.cpython-312.pyc\
│  ├── cache.py\
│  ├── googleai.py\
│  ├── transformer.py\
│  └── utils.py\
├── __pycache_\_\
│  └── main.cpython-312.pyc\
├── .env\
├── main.py\
└── opinions.json


## Prerequisites
- FastAPI
- Google Gemini API and it's key
- YFinance Library
- NewsAPI and it's key
- Postman 
- PyTorch (**OPTIONAL**)


## Installation
Use [pip](https://pip.pypa.io/en/stable/) package manager to install the aforementioned libraries using the following code in bash:
```bash
pip install FastAPI
```

## Usage

- Install [Postman](https://www.postman.com/downloads/) 
- Get your own [Google Gemini API Key](https://ai.google.dev/gemini-api/docs?gad_source=1&gclid=Cj0KCQiAsaS7BhDPARIsAAX5cSByQW_erb7hXf47PIpeGhmwwASiLEkhNLsPtIhrNL8Bx9P-PmubwBIaAubZEALw_wcB) and [NewsAPI Key](https://newsapi.ai/?gad_source=1&gclid=Cj0KCQiAsaS7BhDPARIsAAX5cSDXiE1E9O-FczVsYtXvu8gRVkZ5d0IzrTGN0xOPqA74eLSuIQI4ot4aAonREALw_wcB)
- Store the above keys in the .env file to the root folder
- In the directory for StockMarketApp type into the bash:
```bash
uvicorn main:app
```
- After the server is initialized, log into postman
- Select the GET request in the URL bar and give the following URL in the bar, which acts as your basic link for the server:
```
https://127.0.0.1:8000
```
- Add the following extensions in the URL to access the specific functionality in the program:
```
Replace {symb} with your preferred stock(eg. AAPL, MSFT, META, etc.)
/stock/{symb}           #Stock details
/daily_change/{symb}    #Daily Change 
/moving_average/{symb}  #Moving average
/verdict/{symb}         #Gemini's opinion for the stock
/news/{symb}            #News articles for the stock
/predict/{symb}         #To predict the price of stock for tomorrow

```
- Postman will return the information for the chosen query
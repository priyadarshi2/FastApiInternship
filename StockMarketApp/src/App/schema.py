from pydantic import BaseModel
from datetime import datetime
from typing import List

class StockData(BaseModel):
    symbol: str

class StockDataResponse(StockData):
    data: List[dict]

class DailyChangeResponse(StockData):
    change: List[dict]

class MovingAverageResponse(StockData):
    moving_average: List[dict]

class PredictionBase(StockData):
    prediction: list

class VerdictBase(StockData):
    toBuy : str

class MetricsModel(StockData):
    start_date : str
    end_date : str
    Metrics : dict

class CustomMetrics(StockData):
    start_date : str
    end_date : str
    strats : dict
    Metrics : dict

class StrategyList(BaseModel):
    data : dict

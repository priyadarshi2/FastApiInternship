from fastapi import APIRouter, HTTPException, Request
from src.App.schema import StockDataResponse, DailyChangeResponse, MovingAverageResponse
import src.App.services as srv

router = APIRouter()

@router.get("/stock/{symbol}", response_model=StockDataResponse)
async def show_stock_data(symbol : str,  request : Request):
    start_date = request.query_params.get('start_date',"")
    end_date = request.query_params.get('end_date',"")
    if not symbol or not start_date or not end_date:
        raise HTTPException(status_code=400, detail="Insufficient data")
    if start_date > end_date:
        raise HTTPException(status_code=406, detail="Wrong dates entry")
    else:
        return srv.get_data(symbol, start_date, end_date)

@router.get("/daily_change/{symbol}", response_model=DailyChangeResponse)
async def show_daily_change(symbol : str, request : Request):
    """fjhghjgkhhkj"""
    start_date = request.query_params.get('start_date',"")
    end_date = request.query_params.get('end_date',"")
    if not symbol or not start_date or not end_date:
        raise HTTPException(status_code=400, detail="Insufficient data")
    if start_date > end_date:
        raise HTTPException(status_code=406, detail="Wrong dates entry")
    else:
        return srv.get_daily_change(symbol, start_date, end_date)
    
@router.get("/moving_average/{symbol}", response_model=MovingAverageResponse)
async def show_moving_average(symbol : str, request : Request):
    start_date = request.query_params.get('start_date',"")
    end_date = request.query_params.get('end_date',"")
    window = int(request.query_params.get('window',7))
    if not symbol or not start_date or not end_date or not window:
        raise HTTPException(status_code=400, detail="Insufficient data")
    if start_date > end_date:
        raise HTTPException(status_code=406, detail="Wrong dates entry")
    else:
        return srv.get_moving_average(symbol, window, start_date, end_date)


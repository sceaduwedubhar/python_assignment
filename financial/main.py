from dotenv import load_dotenv
from typing import Union
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi import FastAPI
from datetime import datetime

import os
import sys
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model import FinancialData

load_dotenv()

dbUser = os.getenv("DBUSER")
dbPassword = os.getenv("DBPASSWORD")
dbURL = os.getenv("DBURL")
dbPort = os.getenv("DBPORT")
dbSchema = os.getenv("DBSCHEMA")
api_key = os.getenv("APIKEY")

engine = create_engine(
    f"postgresql+psycopg2://{dbUser}:{dbPassword}@{dbURL}:{dbPort}/{dbSchema}"
)

Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()


@app.get("/api/financial_data")
async def financial_data(
    start_date: Union[str, None] = None,
    end_date: Union[str, None] = None,
    symbol: Union[str, None] = None,
    limit: int = 5,
    page: int = 1,
):
    data = []
    count = 0
    error = ""
    try:
        sess = Session()
        query = sess.query(FinancialData)
        if start_date:
            datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(FinancialData.date >= start_date)
        if end_date:
            datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(FinancialData.date <= end_date)
        if symbol:
            query = query.filter(FinancialData.symbol == symbol)
        count = query.count()
        query = (
            query.order_by(FinancialData.symbol, FinancialData.date)
            .limit(limit)
            .offset((page - 1) * limit)
        )
        results = query.all()

        data = [
            {
                "symbol": result.symbol,
                "date": result.date,
                "open_price": result.open_price,
                "close_price": result.close_price,
                "volume": result.volume,
            }
            for result in results
        ]
    except Exception as e:
        error = str(e)
    finally:
        sess.close()

    return {
        "data": data,
        "pagination": {
            "count": count,
            "page": page,
            "limit": limit,
            "pages": math.ceil(count / limit),
        },
        "info": {"error": error},
    }


@app.get("/api/statistics")
async def read_item(start_date: str, end_date: str, symbol: str):
    aver_open = 0
    aver_close = 0
    aver_vol = 0
    error = ""
    try:
        sess = Session()
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
        query = sess.query(FinancialData)
        query.filter(FinancialData.date >= start_date).filter(
            FinancialData.date <= end_date
        ).filter(FinancialData.symbol == symbol)
        count = query.count()
        results = query.all()

        if count > 0:
            aver_open = sum(result.open_price for result in results) / count
            aver_close = sum(result.close_price for result in results) / count
            aver_vol = sum(result.volume for result in results) / count
    except Exception as e:
        error = str(e)
    finally:
        sess.close()

    return {
        "data": {
            "start_date": start_date,
            "end_date": end_date,
            "symbol": symbol,
            "average_daily_open_price": f"{aver_open:.2f}",
            "average_daily_close_price": f"{aver_close:.2f}",
            "average_daily_volume": f"{aver_vol:.2f}",
        },
        "info": {"error": error},
    }

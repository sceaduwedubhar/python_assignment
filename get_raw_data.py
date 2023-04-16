from sqlalchemy import create_engine
import requests
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from model import FinancialData
from dotenv import load_dotenv
import os

load_dotenv()

dbUser = os.getenv("DBUSER")
dbPassword = os.getenv("DBPASSWORD")
dbURL = os.getenv("DBURL")
dbPort = os.getenv("DBPORT")
dbSchema = os.getenv("DBSCHEMA")
api_key = os.getenv("APIKEY")
api_url = os.getenv("APIURL")

stocks = ["IBM", "AAPL"]

engine = create_engine(
    f"postgresql+psycopg2://{dbUser}:{dbPassword}@{dbURL}:{dbPort}/{dbSchema}"
)

Session = sessionmaker(bind=engine)

today = datetime.today()

for symbol in stocks:
    try:
        url = f"{api_url}&symbol={symbol}"
        r = requests.get(url)
        data = r.json().get("Time Series (Daily)")

        if data is not None:
            for k, v in data.items():
                dateVal = datetime.strptime(k, "%Y-%m-%d")
                if (today - dateVal).days < 14:
                    try:
                        sess = Session()
                        query = (
                            sess.query(FinancialData)
                            .filter(FinancialData.symbol == symbol)
                            .filter(FinancialData.date == dateVal)
                        )
                        if query.count() == 0:
                            fd = FinancialData(
                                symbol=symbol,
                                date=k,
                                open_price=v["1. open"],
                                close_price=v["4. close"],
                                volume=v["6. volume"],
                            )
                            sess.add(fd)
                            sess.commit()
                    except Exception as err:
                        print(err)
                    finally:
                        sess.close()

    except requests.exceptions.RequestException as err:
        print(f"Unable to request {symbol} data. Error: ", err)

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Float
from dotenv import load_dotenv
import os
load_dotenv()

dbUser = os.getenv('DBUSER')
dbPassword = os.getenv('DBPASSWORD')
dbURL = os.getenv('DBURL')
dbPort = os.getenv('DBPORT')
dbSchema = os.getenv('DBSCHEMA')

engine = create_engine(
    f"postgresql+psycopg2://{dbUser}:{dbPassword}@{dbURL}:{dbPort}/{dbSchema}")

Base = declarative_base()


class FinancialData(Base):
    __tablename__ = 'financial_data'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    date = Column(Date)
    open_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)


Base.metadata.create_all(engine)

from sqlalchemy import create_engine, Column, Integer, DateTime, Float
from sqlalchemy.orm import DeclarativeBase
import datetime


class Base(DeclarativeBase):
    pass


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.now())
    rate = Column(Float)


class Engine:
    def __init__(self):
        self.engine = create_engine("sqlite:///exchange_rates.db")
        Base.metadata.create_all(self.engine)

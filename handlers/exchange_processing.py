import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .db import Engine, ExchangeRate
import openpyxl
import aioschedule
import asyncio
from datetime import date
from sqlalchemy import func
import os


def write_to_file():
    today = date.today()

    with Session(autoflush=False, bind=Engine().engine) as db:
        result = (
            db.query(ExchangeRate.date, ExchangeRate.rate)
            .filter(func.date(ExchangeRate.date) == today)
            .all()
        )
    if not result:
        pass
    workbook = openpyxl.Workbook()

    sheet = workbook.active
    headers = ["datetime", "exchange_rate"]
    sheet.append(headers)

    for row in result:
        sheet.append(list(row))

    file_name = f"Exchange UAH-USD {today}.xlsx"
    workbook.save(os.path.join("rates", file_name))

    return file_name


def save_exchange_rate(rate):
    with Session(autoflush=False, bind=Engine().engine) as db:
        exchange_rate = ExchangeRate(rate=rate)
        db.add(exchange_rate)
        db.commit()


async def exchange_request_uah():
    url = "https://www.google.com/finance/quote/USD-UAH"

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    last_price_element = soup.select_one("[data-last-price]")

    if last_price_element:
        last_price = last_price_element.get("data-last-price")
        # print(f"Last price: {last_price}")
        save_exchange_rate(float(last_price))
    else:
        # print("Failed to extract last price")
        return None


async def update_exchange_rate():
    aioschedule.every(1).minutes.do(exchange_request_uah)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(10)


if __name__ == "__main__":
    update_exchange_rate()

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from classes.db import Engine, ExchangeRate
import openpyxl
import aioschedule
import asyncio
from datetime import date
from sqlalchemy import func
import os
from classes.logger import Logger
from config_reader import config

logger = Logger()

def get_today_rate_from_db(date: date):
    """
    Retrieves exchange rate that was collected today
    Args:
        date (date): todays date
    """
    with Session(autoflush=False, bind=Engine().engine) as db:
        result = (
            db.query(ExchangeRate.date, ExchangeRate.rate)
            .filter(func.date(ExchangeRate.date) == date)
            .all()
        )

    if not result:
        logger.error("Impossible to retrieve data from db")



def write_to_file():
    """
    Writes exchange rate to the file with todays date 

    Returns:
        str: name of file, where exchange rates are saved
    """
    today = date.today()

    today_rates = get_today_rate_from_db(today)

    workbook = openpyxl.Workbook()

    sheet = workbook.active
    headers = ["datetime", "exchange_rate"]
    sheet.append(headers)

    for row in today_rates:
        sheet.append(list(row))

    file_name = f"Exchange USD-UAH {today}.xlsx"
    workbook.save(os.path.join("rates", file_name))

    return file_name


def save_exchange_rate(rate: float):
    """
    Saves new exchange rate value into database

    Args:
        rate (float): exchange rate of currency
    """
    with Session(autoflush=False, bind=Engine().engine) as db:
        exchange_rate = ExchangeRate(rate=rate)
        db.add(exchange_rate)
        db.commit()

async def exchange_request_uah():
    """
    Retrieves data from currency exchange website

    Returns:
        none: returns None in case of no data 
    """
    url = config.url.get_secret_value()

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    last_price_element = soup.select_one("[data-last-price]")

    if last_price_element:
        last_price = last_price_element.get("data-last-price")
        logger.info(f"Last rate is {last_price}")
        save_exchange_rate(float(last_price))
    else:
        logger.error("Unable to retrieve exchange rate from site")
        return None

# Scheduler task
async def schedule_exchange_retrieve_request():
    """
    Schedules time when request for new exchange rate will be perfomed
    """

    aioschedule.every(1).minutes.do(exchange_request_uah)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(10)


if __name__ == "__main__":
    schedule_exchange_retrieve_request()

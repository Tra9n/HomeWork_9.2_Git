import datetime
import json
import logging
import os
import time
from bisect import bisect
from json import JSONDecodeError

import pandas as pd
import requests
from dotenv import load_dotenv
from requests import Response

from config import ROOT_DIR

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_KEY_ALPHAVANTAGE = os.getenv("API_KEY_ALPHAVANTAGE")

if not API_KEY:
    raise ValueError("API_KEY не задан в .env")
if not API_KEY_ALPHAVANTAGE:
    raise ValueError("API_KEY_ALPHAVANTAGE не задан в .env")

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(f"{ROOT_DIR}/logs/{__name__}.log", "w", "utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def greet() -> str:
    """Приветствие в формате "???", где ??? — «Доброе утро» / «Добрый день» / «Добрый вечер» /
    «Доброй ночи» в зависимости от текущего времени."""
    hour = datetime.datetime.now().hour

    times = [6, 12, 18]
    greetings = [
        "Доброй ночи",
        "Доброе утро",
        "Добрый день",
        "Добрый вечер",
    ]
    index = bisect(times, hour)
    greeting = greetings[index]
    logger.debug("Выбрано приветствие")
    return greeting


def read_xlsx(path: str) -> pd.DataFrame:
    """Функция чтения из excel файла"""
    logger.info("read_xlsx Запуск функции чтения файла Excel.")
    df: pd.DataFrame = pd.read_excel(path)
    logger.info("Возврат чтения файла Excel.")
    return df


def read_settings(path: str) -> dict | str:
    """Чтение файла настроек пользователя"""
    logger.info("read_settings Чтения файла настроек пользователя")
    try:
        with open(path, "r", encoding="utf-8") as f:
            logger.info("read_settings открытие файла для чтение")
            settings: dict = dict(json.load(f))
    except (FileNotFoundError, JSONDecodeError) as e:
        logger.info(f"read_settings Ошибка{e}")
        return "Проверьте путь и содержимое файла"
    logger.info("read_settings Возврат файла")
    return settings


def card_summary(df: pd.DataFrame) -> list[dict]:
    """По каждой карте:
    последние 4 цифры карты;
    общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей).
    """
    logger.info("card_summary Запуск функции")
    card_list: list = []
    group_card: pd.DataFrame = df.groupby("Номер карты").agg({"Сумма операции с округлением": "sum"})
    for card, sum_oper in group_card.iterrows():
        total = sum_oper.sum()
        cash = round(total / 100, 2)
        card_list.append({"last_digits": card, "total_spent": float(total), "cashback": float(cash)})
    logger.info("card_summary возврат функции")
    return card_list


def top_transactions(df: pd.DataFrame) -> list[dict]:
    """
    Топ 5 транзакций по сумме платежа
    """
    logger.info("top_transactions Запуск функции")
    card_list: list = []
    df = df[(df["Категория"].notna()) & (df["Сумма операции"] < 0)]
    group_card: pd.DataFrame = df.sort_values(by="Сумма операции с округлением", ascending=False)[:5]
    for card, sum_oper in group_card.iterrows():
        date: str = sum_oper["Дата платежа"]
        amount: float = sum_oper["Сумма операции с округлением"]
        category: str = sum_oper["Категория"]
        description: str = sum_oper["Описание"]
        card_list.append({"date": date, "amount": amount, "category": category, "description": description})
    logger.info("top_transactions возврат функции")
    return card_list


def currency_rates(settings: dict) -> list[dict]:
    """Курс валют"""
    logger.info("currency_rates Запуск функции")
    result_data_rates: list = []
    for currency in settings.get("user_currencies", []):
        date: str = datetime.datetime.now().strftime("%Y-%m-%d")
        url: str = f"https://api.apilayer.com/exchangerates_data/{date}"
        params: dict = {"base": currency, "symbols": "RUB"}
        time.sleep(1)
        response: Response = requests.get(url, headers={"apikey": API_KEY}, params=params) # type: ignore
        response.raise_for_status()
        try:
            data: dict = response.json()
            rates: float = data.get("rates", {}).get("RUB", 0.0)
        except JSONDecodeError:
            logger.error("currency_rates")
            rates = 0.0

        result_data_rates.append({"currency": currency, "rate": rates})
    logger.info("currency_rates возврат функции")
    return result_data_rates


def stock_prices(settings: dict) -> list[dict]:
    """Стоимость акций из S&P500"""
    logger.info("stock_prices Запуск функции")
    result_data_stocks: list = []
    for user_stock in settings.get("user_stocks", []):
        url: str = "https://www.alphavantage.co/query"
        params: dict = {
            "function": "GLOBAL_QUOTE",
            "symbol": user_stock,
            "apikey": API_KEY_ALPHAVANTAGE,
        }
        time.sleep(1)
        response: Response = requests.get(url, params=params)
        response.raise_for_status()
        try:
            data: dict = response.json()
            get_price: int | str = data.get("Global Quote", {}).get("05. price", 0)
            prices: float = round(float(get_price), 2)
        except JSONDecodeError:
            logger.error("stock_prices")
            prices = 0.0

        result_data_stocks.append({"stock": user_stock, "price": prices})
    logger.info("stock_prices возврат функции")
    return result_data_stocks

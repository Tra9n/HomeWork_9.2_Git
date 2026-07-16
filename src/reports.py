import logging
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd

from config import ROOT_DIR

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(f"{ROOT_DIR}/logs/{__name__}.log", "w", "utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def write_log(message: pd.DataFrame, file_name: str) -> None:
    """функция записывает результат выполнения функции в файл."""
    logger.info("read_xlsx Запуск функции записи результата выполнения функции foo в файл.")
    to_dict = message.to_dict("records")
    with open(f"{ROOT_DIR}/logs/{file_name}.log", "w", encoding="utf-8") as f:
        f.write(str(to_dict))


def log(filename: str = "default_report.log") -> Callable:
    """Декоратор для логирования с настройками."""
    logger.info("read_xlsx Запуск декоратор для логирования с настройками.")

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Any:
            try:
                result: pd.DataFrame = func(*args, **kwargs)
                logger.info(f"{func.__name__} - OK - {result}\n")
                if isinstance(result, pd.DataFrame):
                    write_log(result, filename)
                return result
            except Exception as e:
                logger.info(f"{func.__name__} - {type(e)} - args: {args}, kwargs: {kwargs}\n")
                raise ValueError("Произошла ошибка декоратора")

        return wrapper

    return decorator


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    logger.info("spending_by_category Запуск функции.")
    if transactions is None:
        raise ValueError("transactions не может быть None")

    if date is None:
        end_date: datetime = datetime.now()
    else:
        end_date = datetime.strptime(date, "%d.%m.%Y")
    start_date: datetime = end_date - pd.DateOffset(months=3)
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y", dayfirst=True)
    filter_data: pd.DataFrame = transactions[
        (transactions["Дата платежа"] >= start_date) & (transactions["Дата платежа"] <= end_date)
    ]
    df: pd.DataFrame = filter_data[filter_data["Категория"] == category]

    logger.info("Возврат функции")
    return df

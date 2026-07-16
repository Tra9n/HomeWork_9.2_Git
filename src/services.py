import calendar
import json
import logging
from datetime import datetime

from config import ROOT_DIR

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(f"{ROOT_DIR}/logs/{__name__}.log", "w", "utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def increased_cashback(data: list[dict], year: int, month: int) -> str:
    """Функция для анализа выгодности категорий повышенного кешбэка."""
    logger.info("increased_cashback Запуск функции для анализа выгодности категорий повышенного кешбэка.")
    start_date: datetime = datetime(year, month, 1)
    weekday, last_day = calendar.monthrange(year, month)
    end_date: datetime = datetime(year, month, last_day)

    result_data: dict = {}
    for item in data:
        if isinstance(item["Дата платежа"], str):
            date_pay: datetime = datetime.strptime(item["Дата платежа"], "%d.%m.%Y")
            if start_date <= date_pay <= end_date and item["Кэшбэк"] > 0:
                category: str = item["Категория"]
                cash: float = float(item["Кэшбэк"])
                if category not in result_data:
                    result_data[category] = 0
                result_data[category] += cash
    sorted_data: list = sorted(result_data.items(), key=lambda x: x[1], reverse=True)
    logger.info("increased_cashback возврат функции.")
    return json.dumps([{k: v} for k, v in sorted_data])

import json

from config import PATH_EXCEL, PATH_SETTINGS_USER
from src.utils import card_summary, currency_rates, greet, read_settings, read_xlsx, stock_prices, top_transactions

type res_data_type = dict[str, str | list[dict]]


def main_data(data: str) -> str:
    try:
        data_excel = read_xlsx(PATH_EXCEL)
        settings_user = read_settings(PATH_SETTINGS_USER)
        if not isinstance(settings_user, dict):
            return json.dumps({"error": "Не удалось загрузить настройки пользователя"})

        result_data = {
            "greet": greet(),
            "cards": card_summary(data_excel),
            "top_transactions": top_transactions(data_excel),
            "currency_rates": currency_rates(settings_user),
            "stock_prices": stock_prices(settings_user),
        }

        return json.dumps(result_data, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Внутренняя ошибка: {str(e)}"})

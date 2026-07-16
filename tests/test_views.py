import json
from unittest.mock import MagicMock, patch

import pytest

from src.views import main_data


@pytest.fixture
def settings_fixture():
    return {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}


@patch("src.views.stock_prices")
@patch("src.views.currency_rates")
@patch("src.views.top_transactions")
@patch("src.views.card_summary")
@patch("src.views.greet")
@patch("src.views.read_settings")
@patch("src.views.read_xlsx")
def test_main_data_success(
    mock_read_xlsx,
    mock_read_settings,
    mock_greet,
    mock_card_summary,
    mock_top_transactions,
    mock_currency_rates,
    mock_stock_prices,
    settings_fixture,
):

    mock_read_xlsx.return_value = MagicMock()
    mock_read_settings.return_value = settings_fixture
    mock_greet.return_value = "Добрый день"
    mock_card_summary.return_value = [{"last_digits": "*1234", "total_spent": 100.0, "cashback": 1.0}]
    mock_top_transactions.return_value = [
        {"date": "01.01.2023", "amount": 500.0, "category": "Еда", "description": "Магазин"}
    ]
    mock_currency_rates.return_value = [{"currency": "USD", "rate": 75.5}]
    mock_stock_prices.return_value = [{"stock": "AAPL", "price": 150.0}]

    result = main_data("")
    data = json.loads(result)

    assert "greet" in data
    assert data["greet"] == "Добрый день"
    assert "cards" in data
    assert "top_transactions" in data
    assert "currency_rates" in data
    assert "stock_prices" in data
    assert len(data["cards"]) == 1
    assert data["cards"][0]["last_digits"] == "*1234"


@patch("src.views.read_settings")
def test_main_data_settings_error(mock_read_settings):
    mock_read_settings.return_value = "Ошибка чтения файла"

    result = main_data("")
    data = json.loads(result)

    assert "error" in data
    assert data["error"] == "Не удалось загрузить настройки пользователя"

from json import JSONDecodeError
from unittest.mock import mock_open, patch

import pytest
from freezegun import freeze_time
from pandas import DataFrame

from src.utils import card_summary, currency_rates, greet, read_settings, read_xlsx, stock_prices, top_transactions


@pytest.mark.parametrize(
    "frozen_time, expected",
    [
        ("2023-01-01 05:00:00", "Доброй ночи"),
        ("2023-01-01 06:00:00", "Доброе утро"),
        ("2023-01-01 11:59:59", "Доброе утро"),
        ("2023-01-01 12:00:00", "Добрый день"),
        ("2023-01-01 17:59:59", "Добрый день"),
        ("2023-01-01 18:00:00", "Добрый вечер"),
        ("2023-01-01 23:59:59", "Добрый вечер"),
        ("2023-01-01 00:00:00", "Доброй ночи"),
    ],
)
def test_greet(frozen_time: str, expected: str) -> None:
    with freeze_time(frozen_time):
        assert greet() == expected


def test_read_excel() -> None:
    with patch("pandas.read_excel") as mock_excel:
        mock_excel.return_value = DataFrame([])
        assert read_xlsx("").empty


@pytest.mark.parametrize(
    "read_data, expected", [('{"1":"1"}', {"1": "1"}), ('{1":"1"}', "Проверьте путь и содержимое файла")]
)
def test_read_settings(read_data: str, expected: dict[str, str] | str) -> None:
    with patch("builtins.open", mock_open(read_data=read_data)):
        assert read_settings("") == expected


def test_card_summary(card_transactions: DataFrame) -> None:
    assert card_summary(card_transactions) == [
        {"cashback": 3.37, "last_digits": "*7197", "total_spent": 337.0},
        {"cashback": 30.0, "last_digits": "*7333", "total_spent": 3000.0},
    ]


def test_top_transactions(card_transactions: DataFrame) -> None:
    assert top_transactions(card_transactions) == [
        {"amount": 3000.0, "category": "Переводы", "date": "01.07.2020", "description": "Линзомат ТЦ Юность"},
        {"amount": 316.0, "category": "Дом и ремонт", "date": "04.02.2019", "description": "OOO Balid"},
        {"amount": 21.0, "category": "Красота", "date": "05.04.2018", "description": "OOO Balid"},
    ]


def test_currency_rates(settings: dict) -> None:
    with patch("requests.get") as mock_req:
        mock_req.return_value.status_code = 200
        mock_req.return_value.json.return_value = {"rates": {"RUB": 1.2}}
        assert currency_rates(settings) == [{"currency": "USD", "rate": 1.2}]
        mock_req.return_value.json.side_effect = JSONDecodeError("", "", 2)
        assert currency_rates(settings) == [{"currency": "USD", "rate": 0.0}]


def test_stock_prices(settings: dict) -> None:
    with patch("requests.get") as mock_req:
        mock_req.return_value.status_code = 200
        mock_req.return_value.json.return_value = {"Global Quote": {"05. price": "21.2"}}
        assert stock_prices(settings) == [{"price": 21.2, "stock": "AAPL"}]

        mock_req.return_value.json.side_effect = JSONDecodeError("", "", 2)
        assert stock_prices(settings) == [{"price": 0.0, "stock": "AAPL"}]

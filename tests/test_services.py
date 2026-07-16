import json

import pandas as pd
import pytest

from src.services import increased_cashback


@pytest.mark.parametrize(
    "year, month, expected",
    [
        (2020, 7, [{"Переводы": 12.0}]),
        (2019, 2, [{"Дом и ремонт": 599.0}]),
        (2018, 4, [{"Красота": 439.0}]),
    ],
)
def test_increased_cashback(card_transactions: pd.DataFrame, year: int, month: int, expected: list[dict]) -> None:
    data = card_transactions.to_dict("records")
    result = increased_cashback(data, year, month)
    assert json.loads(result) == expected

import pandas as pd
import pytest

from src.reports import spending_by_category


def test_spending_by_category(card_transactions: pd.DataFrame) -> None:
    assert not spending_by_category(card_transactions, "Красота", "30.04.2018").empty
    assert spending_by_category(card_transactions, "Красота").empty
    with pytest.raises(ValueError):
        spending_by_category(None, "")

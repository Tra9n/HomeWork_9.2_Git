from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_namber: str) -> str:
    """
    Функция которая умеет обрабатывать информацию как о картах,
     так и о счетах.
    """
    if card_namber[-20:].isdigit():
        return f"Счет {get_mask_account(card_namber[-20:])}"
    else:
        return f"{card_namber[:-16]} {get_mask_card_number(card_namber[-16:])}"


def get_data(time_card: str) -> str:
    """
    Принимает системную дату/время, возвращает
    дату в формате ДД.ММ.ГГГГ
    """
    return time_card[8:10] + "." + time_card[5:7] + "." + time_card[:4]


if __name__ == "__main__":
    print(mask_account_card("MasterCard 7158300734726758"))
    print(mask_account_card("Счет 64686473678894779589"))

def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску"""
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


get_mask_card_number(input())


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску"""
    return f"**{account_number[-4:]}"


get_mask_account(input())

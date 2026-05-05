from typing import Union


def get_mask_card_number(number_card: Union[str]) -> Union[str]:
    """Функцию маскировки номера банковской карты"""
    card_number_str = number_card.replace(" ", "")
    return card_number_str[:4] + " " + card_number_str[4:6] + "** **** " + card_number_str[-4:]


def get_mask_account(number_chek: Union[str]) -> Union[str]:
    """Функцию маскировки номера банковского счета"""
    chek_number_str = number_chek.replace(" ", "")
    return "**" + chek_number_str[-4:]

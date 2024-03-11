import datetime
import json_keys2

PAYMENT_SYSTEMS = ("maestro", "mastercard", "visa", "мир")
ACCOUNT = ("счет", "счёт")


def format_operations(ls: list) -> list:
    """
    Преобразует список операций к форматированному виду.
    см. format_single_operation
    :param ls: Список операций
    :return: Список форматированных операций
    """
    return [format_single_operation(item) for item in ls]


def format_single_operation(operation: dict) -> str:
    """
    Преобразует словарь, содержащий данные банковской операции к формату вида

    "14.10.2018 Перевод организации
    Visa Platinum 7000 79** **** 6361 -> Счет **9638
    82771.72 руб."

    :param operation: Словарь с данными операции
    :return: форматированная строка с данными операции
    """
    date = format_date(operation[json_keys2.KEY_DATE])
    transfer_from = format_card_or_account(operation[json_keys2.KEY_FROM])
    transfer_to = format_card_or_account(operation[json_keys2.KEY_TO])
    operation_amount = operation[json_keys2.KEY_OPERATION_AMOUNT]
    amount = format_amount(operation_amount[json_keys2.KEY_AMOUNT], operation_amount[json_keys2.KEY_CURRENCY])

    return (f"{date} {operation[json_keys2.KEY_DESCRIPTION]}\n"
            f"{transfer_from} -> {transfer_to}\n"
            f"{amount}")


def format_date(date: str) -> str:
    """
    Форматирует исходную дату формата ISO в дату формата dd.mm.yyyy
    :param date: строка даты в формате ISO ("2018-08-17T03:57:28.607101")
    :return: дата формата dd.mm.yyyy (17.08.2018)
    """
    return datetime.datetime.fromisoformat(date).strftime("%d.%m.%Y")


def format_card_or_account(card_or_account: str) -> str:
    """
    Форматирует строку счета или банковской карты к заданному виду.
    Строка счета должна обязательно содержать в себе "счет", "счёт".
    Строка банковской карты должна обязательно содержать в себе "maestro", "mastercard", "visa", "мир"
    :param card_or_account: Строка счета в формате "Счет 72645194281643232984"
    или банковской карты в формате "Maestro 1913883747791351"
    :return: Форматированная строка вида "Счет **2984" или "Maestro 1913 88** **** 1351"
    """
    card_or_account_lower = card_or_account.lower()
    if any(ps in card_or_account_lower for ps in PAYMENT_SYSTEMS):
        return format_card(card_or_account)
    elif any(acc in card_or_account_lower for acc in ACCOUNT):
        return format_account(card_or_account)
    else:
        assert "Unknown"


def format_card(card: str) -> str:
    """
    Форматирует строку вида "Maestro 1913883747791351"
    :param card: строка в формате "Maestro 1913883747791351"
    :return: Форматированная строка вида "Maestro 1913 88** **** 1351"
    """
    # Согласно имеющемуся формату номер карты отделен пробелом от банковской системы
    # и представлен монолитной цифровой строкой
    card_split = card.split()
    payment_system = " ".join(card_split[:-1])
    card_num = card_split[-1]
    assert len(card_num) == 16
    return f"{payment_system} {card_num[:4]} {card_num[4:6]}** **** {card_num[-4:]}"


def format_account(account: str) -> str:
    """
    Форматирует строку вида "Счет 72645194281643232984"
    :param account: строка в формате "Счет 72645194281643232984"
    :return: Форматированная строка вида "Счет **2984"
    """
    account_split = account.split()
    account_word = " ".join(account_split[:-1])
    account_num = account_split[-1]
    return f"{account_word} **{account_num[-4:]}"


def format_amount(amount: str, currency: dict) -> str:
    """
    Форматирование строки содержащей количество денег и тип валюты
    :param amount: количество денег
    :param currency: словарь, содержаний ключ "name", где хранится тип валюты
    :return: Форматированная строка вида "82771.72 руб."
    """
    return f"{amount} {currency[json_keys2.KEY_CURRENCY_NAME]}"

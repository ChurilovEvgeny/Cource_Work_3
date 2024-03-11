import datetime

PAYMENT_SYSTEMS = ("maestro", "mastercard", "visa", "мир")
ACCOUNT = ("счет", "счёт")


def format_operations(ls: list) -> list:
    result = []
    for item in ls:
        pass

    return result


def format_single_operation(operation: dict) -> str:
    date = format_date(operation["date"])
    transfer_from = format_card_or_account(operation["from"])
    transfer_to = format_card_or_account(operation["to"])
    amount = format_amount(operation["amount"], operation["currency"])

    s = (f"{date} {operation["description"]}\n"
         f"{transfer_from} -> {transfer_to}\n"
         f"{amount}")

    return s


def format_date(date: str) -> str:
    return datetime.datetime.fromisoformat(date).strftime("%d.%m.%Y")


def format_card_or_account(card_or_account: str) -> str:
    card_or_account_lower = card_or_account.lower()
    if any(ps in card_or_account_lower for ps in PAYMENT_SYSTEMS):
        return format_card(card_or_account)
    elif any(acc in card_or_account_lower for acc in ACCOUNT):
        return format_account(card_or_account)
    else:
        assert "Unknown"


def format_card(card: str) -> str:
    # Согласно имеющемуся формату номер карты отделен пробелом от банковской системы
    # и представлен монолитной цифровой строкой
    card_split = card.split()
    payment_system = " ".join(card_split[:-1])
    card_num = card_split[-1]
    assert len(card_num) == 16
    return f"{payment_system} {card_num[:4]} {card_num[4:6]}** **** {card_num[-4:]}"


def format_account(account: str) -> str:
    account_split = account.split()
    account_word = " ".join(account_split[:-1])
    account_num = account_split[-1]
    return f"{account_word} **{account_num[-4:]}"


def format_amount(amount: str, currency: dict) -> str:
    return f"{amount} {currency["name"]}"

import pytest

import src.string_formatter as sf


def test_format_single_operation():
    d = {
        "id": 957763565,
        "state": "EXECUTED",
        "date": "2019-01-05T00:52:30.108534",
        "operationAmount": {
            "amount": "87941.37",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 46363668439560358409",
        "to": "Счет 18889008294666828266"
    }
    assert True


def test_format_date():
    assert sf.format_date("2018-03-09T23:57:37.537412") == "09.03.2018"
    with pytest.raises(ValueError):
        sf.format_date("any_data")


def test_format_card_or_account():
    assert sf.format_card_or_account("МИР 3766446452238784") == "МИР 3766 44** **** 8784"
    assert sf.format_card_or_account("Visa Gold 8326537236216459") == "Visa Gold 8326 53** **** 6459"
    assert sf.format_card_or_account("MasterCard 6783917276771847") == "MasterCard 6783 91** **** 1847"
    assert sf.format_card_or_account("Maestro 1308795367077170") == "Maestro 1308 79** **** 7170"
    assert sf.format_card_or_account("Счет 46878338893256147528") == "Счет **7528"


def test_format_card():
    assert sf.format_card("МИР 3766446452238784") == "МИР 3766 44** **** 8784"
    assert sf.format_card("Visa Gold 8326537236216459") == "Visa Gold 8326 53** **** 6459"
    assert sf.format_card("MasterCard 6783917276771847") == "MasterCard 6783 91** **** 1847"
    assert sf.format_card("Maestro 1308795367077170") == "Maestro 1308 79** **** 7170"


def test_format_account():
    assert sf.format_account("Счет 46878338893256147528") == "Счет **7528"


def test_format_amount():
    assert sf.format_amount("25780.71", {"name": "руб.", "code": "RUB"}) == "25780.71 руб."
    assert sf.format_amount("92688.46", {"name": "USD.", "code": "USD"}) == "92688.46 USD."

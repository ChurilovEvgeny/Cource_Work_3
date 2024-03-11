import json
from datetime import datetime

PAYMENT_SYSTEMS = ("maestro", "mastercard", "visa", "мир")
ACCOUNT = ("счет", "счёт")
EXECUTED_OPERATION = "EXECUTED"

KEY_STATE = "state"
KEY_DATE = "date"
KEY_DESCRIPTION = "description"

TRANSLATE_FIND_WORD = "ПЕРЕВОД"


def get_formatted_last_executed_operations(json_file_path: str) -> str:
    pass


def get_last_n_executed_transfer_operations(json_file_path: str, n: int = 5):
    if n < 0:
        raise ValueError("The number of operations (n) cannot be less than zero")

    ls = leave_only_executed_transfer_operations(load_json(json_file_path))
    sort_operations_by_datetime(ls)
    return ls[:n]


def load_json(json_file_path: str) -> list:
    """
    Функция открывает файл json и возвращает его, как список
    :param json_file_path: путь к файлу json
    :return: список. Если файл не существует, то активируется исключение FileNotFoundError
    """
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def leave_only_executed_transfer_operations(ls: list) -> list:
    # Так как нет отдельного служебного поля для однозначного поиска типа операции,
    # то приходится искать нужную операцию по косвенному признаку
    # наличия слова "перевод" в описании операции
    return [item for item in ls if
            item.get(KEY_STATE, "").upper() == EXECUTED_OPERATION and
            TRANSLATE_FIND_WORD in item.get(KEY_DESCRIPTION, "").upper()]


def sort_operations_by_datetime(ls: list) -> None:
    # Дата в iso формате обладает таким интересным свойством,
    # что ее не надо переводить в тип datetime через datetime.fromisoformat(),
    # а можно сортировать непосредственно в типе str
    ls.sort(key=lambda x: x[KEY_DATE], reverse=True)

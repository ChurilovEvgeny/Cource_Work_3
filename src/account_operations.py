import json
from datetime import datetime

PAYMENT_SYSTEMS = ("maestro", "mastercard", "visa", "мир")
ACCOUNT = ("счет", "счёт")
EXECUTED_OPERATION = "EXECUTED"

KEY_STATE = "state"
KEY_DATE = "date"

def get_formatted_last_executed_operations(json_file_path: str) -> str:
    pass


def load_json(json_file_path: str) -> list:
    """
    Функция открывает файл json и возвращает его, как список
    :param json_file_path: путь к файлу json
    :return: список. Если файл не существует, то активируется исключение FileNotFoundError
    """
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def leave_only_executed_operations(ls: list) -> list:
    return [item for item in ls if item.get(KEY_STATE, "").upper() == EXECUTED_OPERATION]


def sort_operations_by_datetime(ls: list) -> None:
    
    # Дата в iso формате обладает таким интересным свойством,
    # что ее не надо переводить в тип datetime через datetime.fromisoformat(),
    # а можно сортировать непосредственно в типе str
    ls.sort(key=lambda x: x[KEY_DATE], reverse=True)


# ls = load_json("../test_files/operations.json")
# print(len(ls))
# ls = leave_only_executed_operations(ls)
# print(len(ls))
#
# sort_operations_by_datetime(ls)
# print(len(ls))
# #
# datee = "2019-08-26T10:50:58.294041"
# datetime_str = '09/19/22 13:55:26'
#
# tt = datetime.fromisoformat(datee)
# datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
# datetime_object = datetime.strptime(datetime_str, '%Y-%d-%mT%H:%M:%S.%ms')

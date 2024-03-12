import json
import src.account_operations_json_keys as json_keys
import src.string_formatter as sf

EXECUTED_OPERATION = "executed"
TRANSLATE_FIND_WORD = "перевод"


def get_formatted_last_executed_operations(json_file_path: str, n: int = 5) -> str:
    """
    Функция возвращает полностью отформатированную и готовую для вывода строку, содержащую последние по дате выполенния
    n успешных операций перевод.
    :param json_file_path: Путь к json файлу с операциями пользователя
    :param n: количество возвращаемых операций
    :return: форматированная строка
    """
    ls = get_last_n_executed_transfer_operations(json_file_path, n)
    format = sf.format_operations(ls)
    return "\n\n".join(format)  # Два переноса, так как есть требование иметь пустую строку между операциями


def get_last_n_executed_transfer_operations(json_file_path: str, n: int = 5) -> list:
    """
    Функция возвращает форматированные для отображения строки последних n успешных операций перевода.
    :param json_file_path: Путь к json файлу с операциями пользователя
    :param n: количество возвращаемых операций
    :return: список форматированных для отображения операций
    """
    if n < 0:
        raise ValueError("The number of operations (n) cannot be less than zero")

    ls = leave_only_executed_transfer_operations(load_json(json_file_path))
    sort_operations_by_datetime(ls)
    return ls[:n]


def load_json(json_file_path: str) -> list:
    """
    Функция открывает файл json и возвращает его, как список словарей
    :param json_file_path: путь к файлу json
    :return: список. Если файл не существует, то инициируется исключение FileNotFoundError
    """
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def leave_only_executed_transfer_operations(ls: list) -> list:
    """
    Функция оставляет только выполненные (EXECUTED) операции по переводу.
    :param ls: Исходный список
    :return: Отфильтрованный список
    """
    # Так как нет отдельного служебного поля для однозначного поиска типа операции,
    # то приходится искать нужную операцию по косвенному признаку
    # наличия слова "перевод" в описании операции
    return [item for item in ls if
            item.get(json_keys.KEY_STATE, "").lower() == EXECUTED_OPERATION and
            TRANSLATE_FIND_WORD in item.get(json_keys.KEY_DESCRIPTION, "").lower()]


def sort_operations_by_datetime(ls: list):
    """
    Сортирует передаваемый список по убыванию даты.
    Дата должна быть строка в ISO формате
    Функция модифицирует исходный список
    :param ls: сортируемый список
    """
    # Дата в iso формате обладает таким интересным свойством,
    # что ее не надо переводить в тип datetime через datetime.fromisoformat(),
    # а можно сортировать непосредственно в типе str
    ls.sort(key=lambda x: x[json_keys.KEY_DATE], reverse=True)

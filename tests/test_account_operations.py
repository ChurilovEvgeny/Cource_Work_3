import pytest
import src.account_operations as ac


@pytest.fixture
def data_leave_only_executed_transfer_operations():
    return [
        {
            "state": "EXECUTED",
            "description": "Перевод организации",
        },
        {
            "state": "EXECUTED",
            "description": "Открытие вклада",
        },
        {
            "state": "CANCELED",
        },
        {
            "another": "any",
        },
    ]


def test_load_json_to_dict():
    assert len(ac.load_json("../test_files/operations.json")) > 0
    with pytest.raises(FileNotFoundError):
        ac.load_json("file_not_exist.json")


def test_leave_only_executed_transfer_operations(data_leave_only_executed_transfer_operations):
    assert len(ac.leave_only_executed_transfer_operations([])) == 0
    dt = ac.leave_only_executed_transfer_operations(data_leave_only_executed_transfer_operations)
    assert len(dt) == 1
    assert dt[0][ac.KEY_DESCRIPTION] == "Перевод организации"


def test_sort_operations_by_datetime():
    dt = [
        {
            "date": "2018-03-09T23:57:37.537412",
        },
        {
            "date": "2019-07-13T18:51:29.313309",
        },
        {
            "date": "2019-08-13T18:51:29.313309",
        },
    ]
    ac.sort_operations_by_datetime(dt)
    assert dt[0][ac.KEY_DATE] == "2019-08-13T18:51:29.313309"
    assert dt[1][ac.KEY_DATE] == "2019-07-13T18:51:29.313309"
    assert dt[2][ac.KEY_DATE] == "2018-03-09T23:57:37.537412"


def test_get_last_n_executed_transfer_operations():
    assert len(ac.get_last_n_executed_transfer_operations("../test_files/operations.json")) == 5
    assert len(ac.get_last_n_executed_transfer_operations("../test_files/operations.json", 0)) == 0
    assert len(ac.get_last_n_executed_transfer_operations("../test_files/operations.json", 1)) == 1
    with pytest.raises(ValueError):
        ac.get_last_n_executed_transfer_operations("../test_files/operations.json", -1)

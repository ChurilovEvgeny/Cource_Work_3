import src.account_operations as ac


def main():
    print(ac.get_formatted_last_executed_operations("../tests/test_files/operations.json"))


if __name__ == '__main__':
    main()

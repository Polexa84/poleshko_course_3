import json
from datetime import datetime


def load_operation():
    """"Загружает список операций из файла"""
    with open("operations.json", "r") as list:
        operations_list = json.load(list)
        return operations_list


def read_executed_operation():
    """"Выбирает успешную операцию и сортерует этот список по дате"""
    executed_items = []
    for item in load_operation():
        for key, value in item.items():
            if value == "EXECUTED":
                executed_items.append(item)
    sorted_items = sorted(executed_items, key=lambda x: x['date'])
    return sorted_items


def creates_correct_list():
    """"Раскладывает полученые операции выше и собирает в нужный формат"""

    # Дробовляем переменную и финальную фразу
    count = 0
    result = ""
    # Дробим список и собираем в нужном формате
    operations = read_executed_operation()

    for operation in reversed(operations):
        if count < 5:
            date_str = operation['date'][:10]
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%d.%m.%Y')
            description = operation['description']
            try:
                from_account = operation['from']
            except KeyError:
                from_account = None
            to_account = operation['to']
            amount = operation['operationAmount']['amount']
            currency = operation['operationAmount']['currency']['name']
            if to_account.split()[0] == "Счет":
                to_account = f"{operation['to'].split()[0]} **{operation['to'][-4:]}"
            else:
                to_account = f'{" ".join(operation["to"].split()[:-1])} ' \
                             f'{operation["to"].split()[-1][:4]} {operation["to"].split()[-1][4:6]}** ' \
                             f'**** {operation["to"].split()[-1][-4:]}'

            if from_account is None:
                from_account = "Внесение наличных"
            elif from_account.split()[0] == "Счет":
                from_account = f"{operation['from'].split()[0]} **{operation['from'][-4:]}"
            else:
                from_account = f'{" ".join(operation["from"].split()[:-1])} ' \
                               f'{operation["from"].split()[-1][:4]} {operation["from"].split()[-1][4:6]}** ' \
                               f'**** {operation["from"].split()[-1][-4:]}'

            # Состовляем финальную фразу
            result += f"{formatted_date} {description}\n"
            result += f"{from_account} -> {to_account}\n"
            result += f"{amount} {currency}\n\n"

        count += 1

    return result
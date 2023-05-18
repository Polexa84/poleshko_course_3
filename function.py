# Импортируем библиотеки
import json
from datetime import datetime
import sys

# Импортируем константы
from config import OPERATIONS_FILE, DESIRED_STATUS, MAX_OPERATIONS_NUMBER


def load_operations():
    """Загружает список операций из файла"""
    try:
        with open(OPERATIONS_FILE, "r") as list:
            operations_list = json.load(list)
            return operations_list
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка при загрузке операций! Причина: {e}")
        sys.exit("Устраните ошибку и запустите программу заново!")


def get_sorted_successful_operations():
    """"Выбирает только успешные операцию"""
    executed_items = []
    for item in load_operations():
        for key, value in item.items():
            if value == DESIRED_STATUS:
                executed_items.append(item)
    return executed_items


def get_successful_operations_sorted_by_date():
    """"Успешные операции сортерует по дате"""
    sorted_items = sorted(get_sorted_successful_operations(), key=lambda x: x['date'])
    return sorted_items



def convert_operations_to_correct_format():
    """"Раскладывает полученые операции выше и собирает в нужный формат"""

    # Дробовляем переменную и финальную фразу
    count = 0
    result = ""
    # Дробим список и собираем в нужном формате
    operations = get_successful_operations_sorted_by_date()

    for operation in reversed(operations):
        if count < MAX_OPERATIONS_NUMBER:
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

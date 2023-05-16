import json
from datetime import datetime


def load_operation():
    """"Загружает список операций из файла"""
    with open("operations.json", "r") as list:
        operations_list = json.load(list)
        return operations_list


def read_executed_operation():
    executed_items = []
    for item in load_operation():
        for key, value in item.items():
            if value == "EXECUTED":
                executed_items.append(item)
    return executed_items


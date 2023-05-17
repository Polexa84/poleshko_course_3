import pytest
from function import creates_correct_list, read_executed_operation
import json
from datetime import datetime
from function import load_operation


def test_load_operation():
    data = load_operation()
    assert isinstance(data, list)

def test_creates_correct_list():
    result = creates_correct_list()

    # Прроверка наличия определенных строк в ртзультатах
    assert '08.12.2019 Открытие вклада\n' in result
    assert '07.12.2019 Перевод организации\n' in result
    assert '19.11.2019 Перевод организации\n' in result
    assert '13.11.2019 Перевод со счета на счет\n' in result
    assert '05.11.2019 Открытие вклада\n' in result

    # Прроверка количества строк
    assert len(result.split('\n')) == 21


if __name__ == "__main__":
    pytest.main([__file__])

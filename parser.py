#!/usr/bin/env python3
import sys
import json
import yaml

# Принимать на вход имя файла
if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    print("Ошибка. Должен быть один параметр - имя файла")
    sys.exit()
    # path = "testfile.yaml"
    # path = "testfile.json"
    # для теста

is_yaml = False
is_json = False

# Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
# path = "testfile.yaml"

try:
    with open(path, "r") as file_j:
        data_json = json.load(file_j)
        is_json = True
except json.decoder.JSONDecodeError as json_error:
    json_error_lineno = json_error.lineno
    json_error_msg = json_error.msg
    is_json = False
except FileNotFoundError:
    print("Файл не найден")
    sys.exit(1)

try:
    with open(path, "r") as file_y:
        data_yaml = yaml.safe_load(file_y)
        if data_yaml is None:
            print("Файл пустой!")
            sys.exit(2)
        is_yaml = True
except yaml.YAMLError as yaml_err:
    print(f'Ошибка {yaml_err}')
    pass

# При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер

if not is_json and not is_yaml:
    print(f'Ошибка "{json_error_msg}" в строке {json_error_lineno}')
    sys.exit(3)

# Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
# Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)

if is_json:
    data = data_json
    filename = path[:path.rfind('.')]
    newfilename = filename + "_converted.yaml"
    with open(newfilename, 'w') as f:
        yaml.dump(data, f)
    sys.exit(4)
elif is_yaml:
    data = data_yaml
    filename = path[:path.rfind('.')]
    newfilename = filename + "_converted.json"
    with open(newfilename, 'w') as f:
        json.dump(data, f)
    print(f'Converted - new file is {newfilename}')
    sys.exit(5)
else:
    print('Файл не является форматом JSON или YAML, попробуйте указать другой файл!')
    sys.exit(6)

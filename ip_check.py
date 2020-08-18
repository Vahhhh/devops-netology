import socket
import json
import yaml

hosts_list = ('drive.google.com', 'mail.google.com', 'google.com')
ip_database = {}
ip_database_set = {}
ip_database_prev_j = {}
ip_database_set_prev_j = {}
ip_database_prev_y = {}
ip_database_set_prev_y = {}
is_changed = False

try:
    with open("jsonfile") as file_j: # пробуем прочитать файл
        ip_database_prev_j = json.load(file_j)
        for host in hosts_list: # и преобразовываем значения словаря в set
            ip_database_set_prev_j[host] = set(ip_database_prev_j[host])
# если файл не найден или он не читается как JSON - создаём его и заполняем текущими данными
except (FileNotFoundError, json.decoder.JSONDecodeError):
    for host in hosts_list:
        ip_database_prev_j[host] = socket.gethostbyname_ex(host)[2]
        ip_database_set_prev_j[host] = set(ip_database_prev_j[host])
    with open("jsonfile", "w") as file_j:
        json.dump(ip_database_prev_j, file_j)
    print("Файл с данными JSON пустой или отсутствует - создаём")
    # is_changed = True

try:
    with open("yamlfile") as file_y: # пробуем прочитать файл
        ip_database_prev_y = yaml.safe_load(file_y)
        if ip_database_prev_y:
            for host in hosts_list: # и преобразовываем данные в set
                ip_database_set_prev_y[host] = set(ip_database_prev_y[host])
        else:
            ip_database_prev_y = {}
            for host in hosts_list:
                ip_database_prev_y[host] = socket.gethostbyname_ex(host)[2]
                ip_database_set_prev_y[host] = set(ip_database_prev_y[host])
            with open("yamlfile", "w") as file_y:
                yaml.dump(ip_database_prev_y, file_y)
                print("Файл с данными YAML пустой - наполняем")

# если файл не найден или он не читается как YAML - создаём его и заполняем переменные текущими данными
except (FileNotFoundError):
    for host in hosts_list:
        ip_database_prev_y[host] = socket.gethostbyname_ex(host)[2]
        ip_database_set_prev_y[host] = set(ip_database_prev_y[host])
    with open("yamlfile", "w") as file_y:
        yaml.dump(ip_database_prev_y, file_y)
    # is_changed = True
    print("Файл с данными YAML отсутствует - создаём")


for host in hosts_list:
    ip_database[host] = socket.gethostbyname_ex(host)[2]
    ip_database_set[host] = set(ip_database[host])
    if (ip_database_set[host] == ip_database_set_prev_j[host]) and (ip_database_set[host] == ip_database_set_prev_y[host]):
        pass
    elif ip_database_set[host] == ip_database_set_prev_y[host]:
        print(f'[ERROR] [JSON] {host} IP mismatch: {ip_database_set_prev_j[host]} {ip_database_set[host]}')
        is_changed = True
    elif ip_database_set[host] == ip_database_set_prev_j[host]:
        print(f'[ERROR] [YAML] {host} IP mismatch: {ip_database_set_prev_y[host]} {ip_database_set[host]}')
        is_changed = True
    else:
        print(f'[ERROR] [JSON] {host} IP mismatch: {ip_database_set_prev_j[host]} {ip_database_set[host]}')
        print(f'[ERROR] [YAML] {host} IP mismatch: {ip_database_set_prev_y[host]} {ip_database_set[host]}')
        is_changed = True

if is_changed:
    with open("jsonfile", "w") as file_j:
        json.dump(ip_database, file_j)
    with open("yamlfile", "w") as file_y:
        yaml.dump(ip_database, file_y)
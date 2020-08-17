import socket
import json
import yaml

hosts_list = ('drive.google.com', 'mail.google.com', 'google.com')
ip_database = {}

with open("jsonfile") as file_j:
    ip_database_prev_j = json.load(file_j)
# print(ip_database_prev_j)

with open("yamlfile") as file_y:
    ip_database_prev_y = yaml.safe_load(file_y)
# print(ip_database_prev_y)

is_changed = False

# Самым сложным оказалось разобраться как быть, если в файле нет ключа (забыл как с dict.get работать)
for host in hosts_list:
    ip_database[host]=socket.gethostbyname(host)
    if ip_database[host] != ip_database_prev_j.get(host):
        print(f'[ERROR] [JSON] {host} IP mismatch: {ip_database_prev_j.get(host)} {ip_database[host]}')
        is_changed = True

    if ip_database[host] != ip_database_prev_y.get(host):
        print(f'[ERROR] [YAML] {host} IP mismatch: {ip_database_prev_y.get(host)} {ip_database[host]}')
        is_changed = True

# Придумал куда её засунуть, чтобы лишний раз не дёргать файл, если изменений не было. У нас же высоконагруженные системы :)
# Если ключа не было - тоже запишем.

if is_changed:
    with open("jsonfile", "w") as file_j:
        json.dump(ip_database, file_j)
    with open("yamlfile", "w") as file_y:
        yaml.dump(ip_database, file_y)
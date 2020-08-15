import socket
hosts_list = ('drive.google.com', 'mail.google.com', 'google.com')
ip_database = {}
ip_database_prev = {}
for host in hosts_list:
    ip_database_prev[host]=socket.gethostbyname(host)
    print(f'{host} - {ip_database_prev[host]}') # Выводим исходные данные с первого запроса
while True:
    for host in hosts_list:
        ip_database[host]=socket.gethostbyname(host)
        if ip_database[host] != ip_database_prev[host]:
            print(f'[ERROR] {host} IP mismatch: {ip_database_prev[host]} {ip_database[host]}')
            print(f'{host} - {ip_database[host]}') # Выводим изменившиеся данные
            ip_database_prev = ip_database


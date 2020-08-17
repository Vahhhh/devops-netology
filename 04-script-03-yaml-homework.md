1. Ошибки поправил, вот что получилось:

```
{ "info" : "Sample JSON output from our service\t",
    "elements" : [
        { "name" : "first",
        "type" : "server",
        "ip" : 7175
        },
        { "name" : "second",
        "type" : "proxy",
        "ip" : "71.78.22.43"
        }
    ]
}
```

2. Вот какой скрипт получился (теперь он не постоянно работает, я отрабатывает и сохраняет всё в файл - прикольно ;) ).

```
import socket
import json
hosts_list = ('drive.google.com', 'mail.google.com', 'google.com')
ip_database = {}

with open("jsonfile") as file_j:
    ip_database_prev = json.load(file_j)

for host in hosts_list:
    ip_database[host]=socket.gethostbyname(host)
    if ip_database[host] != ip_database_prev[host]:
        print(f'[ERROR] {host} IP mismatch: {ip_database_prev[host]} {ip_database[host]}')
        ip_database_prev = ip_database

with open("jsonfile", "w") as file_j:
    json.dump(ip_database_prev, file_j)

```

***1. Есть скрипт:***

```
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

- Какое значение будет присвоено переменной c?

Мне кажется, что никакого - появится ошибка, т.к. складываются переменные разных типов. 

- Как получить для переменной c значение 12?

`c = str(a) + b`

- Как получить для переменной c значение 3?

`c = a + int(b)`


***2. Этим скриптом недовольно начальство, потому что в его выводе не хватает изменённых файлов и не понятно, в какой директории они находятся.***

Если я правильно понял задание - я добавил туда вот что: `os.getcwd() + '/' + `
Поправил - убрал break (а зачем он там был? ;))

```
vagrant@vagrant:~/devops-netology$ cat changed.py
#!/usr/bin/env python3

import os

bash_command = ["cd ~/devops-netology", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = os.getcwd() + '/' + result.replace('\tmodified:   ', '')
        print(prepare_result)


vagrant@vagrant:~/devops-netology$ ./changed.py
/home/vagrant/devops-netology/changed2.py
/home/vagrant/devops-netology/has_been_moved.txt
```

***3. Доработать скрипт выше так, чтобы он мог проверять локальный репозиторий в директории, которую мы передаём, как входной параметр.***

Я немного поменял скрипт, убрал 2-й вызов subprocess, однако не очень понимаю, как я могу вывод git'а интерпретировать. В смысле в случае если он запущен не в директории репозитория, он пишет ошибку в stderr, а os.popen вроде как это не умеет - поэтому всё равно subprocess.run надо использовать... Как я понял ;)
Про `is_change = False` - я обдумался, но  не придумал куда и для чего его можно засунуть.. :( Есть ощущение, что я чего-то просто не знаю, поэтому не понимаю как это можно применить.. ;)

```
vagrant@vagrant:~/devops-netology$ cat changed2.py
#!/usr/bin/env python3
#just comment to change file

import subprocess
import sys
import os

if len(sys.argv) == 1:
    path = "~/devops-netology"
elif len(sys.argv) > 2:
    print("Ошибка. Слишком много параметров.")
    sys.exit(1)
else:
    path = sys.argv[1]
bash_command = ["cd " + path, "git status"]
result_os = subprocess.run(' && '.join(bash_command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
if result_os.returncode != 0:
    print("Этот каталог не является каталогом git")
    sys.exit(2)
is_change = False
for result in result_os.stdout.split('\n'):
    if result.find('modified') != -1:
        prepare_result = os.getcwd() + '/' + result.replace('\tmodified:   ', '')
        print(prepare_result)
        
```

Ещё сделал только используя модуль `os`, без `subprocess`, но мне так не нравится - если будет файл с названием fatal или что-то такое - будет косяк.. ;)

```
import sys
import os

if len(sys.argv) == 1:
    path = "~/devops-netology"
elif len(sys.argv) > 2:
    print("Ошибка. Слишком много параметров.")
    sys.exit(1)
else:
    path = sys.argv[1]
bash_command = ["cd " + path, "git status 2>&1"]
result_os = os.popen(' && '.join(bash_command)).read()
if result_os.find('fatal') != -1:
    print("Этот каталог не является каталогом git")
    sys.exit(2)
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = os.getcwd() + '/' + result.replace('\tmodified:   ', '')
        print(prepare_result)
```

***4. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>.***

Я сделал скрипт как сервис - мониторит постоянно и при изменении адреса пишет об этом. Если нужно чтобы запускалось единоразово - примерно понимаю как (хранить в файловой системе) - интересно будет сделать! 

**Это попробую сделать во время выполнения следующего задания - как раз там буду хранить текущее состояние в json'е :)
Плюс по группам адресов - я думал выпендриться через `socket.gethostbyname_ex` знаю про set'ы и про их сравнение (немного пробовал играться), просто в примере было написано про то, что всего 1 IP-адрес у хоста - я и не стал об этом думать.. :) Попробую если время останется после более сложных историй (тут я хотя бы понимаю как делать - вопрос времени)
Единственное только не понял, как сделать демонизацию, и/или что под этим подразумевается ;)**

```
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

```

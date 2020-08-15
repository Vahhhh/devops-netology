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
        break


vagrant@vagrant:~/devops-netology$ ./changed.py
/home/vagrant/devops-netology/changed2.py
```


***3. Доработать скрипт выше так, чтобы он мог проверять локальный репозиторий в директории, которую мы передаём, как входной параметр.***

Учитывая, что я это писал часа 4 - уверен, что будет много неправильного, или не по канонам, что можно было сделать лучше - буду рад любым комментариям!

```
vagrant@vagrant:~/devops-netology$ cat changed2.py
#!/usr/bin/env python3

import subprocess
import sys

if len(sys.argv) == 1:
    path = "~/devops-netology"
elif len(sys.argv) > 2:
    print("Ошибка. Слишком много параметров.")
    sys.exit(1)
else:
    path = sys.argv[1]
bash_command = ["cd " + path, "git status"]
if subprocess.call(' && '.join(bash_command), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
    print("Этот каталог не является каталогом git")
    sys.exit()
result_os = subprocess.run(' && '.join(bash_command), shell=True, stdout=subprocess.PIPE, text=True)
is_change = False
for result in result_os.stdout.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

***4. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>.***

Я сделал скрипт как сервис - мониторит постоянно и при изменении адреса пишет об этом. Если нужно чтобы запускалось единоразово - примерно понимаю как (хранить в файловой системе) - интересно будет сделать!

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

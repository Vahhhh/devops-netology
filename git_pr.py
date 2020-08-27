#!/usr/bin/env python3

import subprocess
import sys
import requests

username = 'Vahhhh'
password = '8e31651cfd88acad6eb4228464f71ff8a1177f8f'

if len(sys.argv) == 2:
    comment = sys.argv[1]
else:
    print("Ошибка. Единственным аргументом при запуске скрипта должен быть комментарий.")
    sys.exit()
    # comment = 'test'  # Это на случай тестирования с PyCharm'а, не из командной строки
bash_command = "git status && git remote -v"
result_os = subprocess.run(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
if result_os.returncode != 0:
    print("Этот каталог не является каталогом git")
    sys.exit()
for result in result_os.stdout.split('\n'):
    if result.find('On branch master') != -1:
        print("Этот скрипт нельзя запускать в master. Его нужно запускать в ветке, которую хотите смёрджить в master")
        sys.exit()
# Узнаём название удалённой ветки
    elif result.find('Your branch is up to date with ') != -1:
        # repository_remote = result[32:-2].split('/')[0]
        branch_remote = result[32:-2].split('/')[1]
# Из настроек remote git'а берём информацию о названии репозитория и имени владельца в строчке, имеющей отношение
# к push github'a. С ssh работать тоже будет - надо только подтюнить - как текст будет написан.
    elif result.find('https://github.com/') != -1 and result.find(' (push)') != -1:
        owner = result.split()[1].split('/')[3]
        repo = result.split()[1].split('/')[4][:-4]
# Создаём url, который будем дёргать
url = 'https://api.github.com/repos/'+ owner + '/' + repo + '/pulls'
payload = {"title": comment, "head": branch_remote, "base": "master"}
r = requests.post(url, json=payload, auth=(username, password))
if r.status_code == 201:
    print(f"Please, visit {r.json()['html_url']} to confirm the pull request")
elif r.status_code == 401:
    print("Ошибка авторизации")
else:
    for i in r.json()['errors']:
        print(f"Произошла ошибка - {i['message']} - исправьте, или перезвоните позже!")

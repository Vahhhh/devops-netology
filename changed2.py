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
    sys.exit()
is_change = False
for result in result_os.stdout.split('\n'):
    if result.find('modified') != -1:
        prepare_result = os.getcwd() + '/' + result.replace('\tmodified:   ', '')
        print(prepare_result)


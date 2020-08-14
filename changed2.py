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


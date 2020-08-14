#!/usr/bin/env python3

import os
import sys

if len(sys.argv) == 1:
    path = "~/devops-netology"
elif len(sys.argv) > 2:
    print("Ошибка. Слишком много параметров.")
    sys.exit(1)
else:
    path = sys.argv[1]
path = "cd " + path
bash_command = [path, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break

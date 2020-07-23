## Домашнее задание к занятию «3.1. Работа в терминале (лекция 1)»

Сначала Vagrant не хотел запускать VM и выдавал ошибку VT-x is not available (VERR_VMX_NO_VMX). Причём не запускал не только новую виртуалку, но также и машину, которую я запускал ранее. Гуглёж показал 3 возможных причины:

VT-x не включен в BIOS
CPU не поддерживает VT-x
Виртуализация Hyper-V включена в Windows

Прошёл по всем вариантам - у меня всё в порядке. Погуглил ещё - посоветовали установить обновления. А у меня как раз прилетели обновления от горячо любимого Microsoft. И через 1,5 часа установки какого-то ключевого обновления всё взлетело! ;)

4. Вообще не знал, что поднятие VM может быть **настолько** простым и автоматизирвоанным ;)
Единственное - выключать через `vagrant shutdown` он мн ене даёт, выключает через `vagrant halt`

Почитал, как конфигурить. Прямо скажем - не очень для меня тривиально оказалось - в документации всё (как по мне так) урезано сильно. Но доки+гугл помогли найти то что надо.

6. Меняем файл Vagrant
```
Vagrant.configure("2") do |config|
	config.vm.box = "bento/ubuntu-20.04"
	config.vm.provider "virtualbox" do |v|
		v.memory = 2048
#		v.cpus = 2
#		v.customize ["modifyvm", :id, "--memory", "2048"]
		v.customize ["modifyvm", :id, "--cpus", "3"]
	end
end
```

8.1. Длина журнала `history` задаётся в переменной HISTSIZE, которая находится на 733-й строчке - `man mash | less -N`, дальше поиск по слову history через `/`. Есть ещё HISTFILESIZE - 721 строчка - количество линий в файле истории, которое по-умолчанию равно HISTSIZE. (кстати не очень понял разницу - по-идее же эта история как раз и хранится в файле - как может переменная HISTFILESIZE быть меньше HISTSIZE, где тогда будет храниться история, если не в файле? ;)
8.2. `ignoreboth` делает так, чтобы в историю не записывались как строчки, начинающиеся с пробела (офигенная штука, не знал об этом до лекции), так и команды, которые даны путём нажатия кнопки "вверх" и их повторного вызова.

9. Про `{}` впервые упоминается на строке 230 и там говорится про список, но я не понял как это, перечитав 3 раза.. Дальше эти символы встречаются на строке 879, где говорится о массивах.
Ну а то, что обсуждалось в Slack'е находится на строке 926 и далее - такие скобки позволяют "раскрыть", или "подставить" необходимые данные, перечисленные через запятую.

10. `touch {000001..100000}.file`
300000 файлов не получилось - вы уже объясняли в Slack почему (жаль сам раньше не успел ДЗ сделать). Но я погуглил ошибку, нашёл ответ на Stackoferflow:
```
It's a kernel limitation on the size of the command line argument. Use a for loop instead.
Origin of problem
This is a system issue, related to execve and ARG_MAX constant. There is plenty of documentation about that (see man execve, debian's wiki).
Basically, the expansion produce a command (with its parameters) that exceeds the ARG_MAX limit. On kernel 2.6.23, the limit was set at 128 kB. This constant has been increased and you can get its value by executing:
getconf ARG_MAX
# 2097152 # on 3.5.0-40-generic
```
Проверил у себя - цифра та же :)

Удалось создать такой командой - `echo {000001..300000}.file | xargs touch`
Заодно научился и удалять... :) - `ls | xargs rm`

11. Весь man перерыл, нашёл про test, [ и [[, но так и не понял как сделать вывод. Максимум к чему приблизился - получилось `echo $[1 > 2]`
Да, нашёл команду... `[[ -d test2 ]] && echo "Dir exist" || echo "Dir does not exist"`
Нашёл ещё более правильную наверно команду - `[[ -d test ]] ; echo $?` - показывает удачно ли выполнена прошлая команда - выдаст 0 если найдена директория и 1 если нет.

12. 
```
vagrant@vagrant:~$ type -a bash
bash is /usr/bin/bash
bash is /bin/bash
vagrant@vagrant:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

vagrant@vagrant:~$ mkdir /tmp/new_path_directory
vagrant@vagrant:~$ cp /bin/bash /tmp/new_path_directory/
vagrant@vagrant:~$ sudo cp /bin/bash /usr/local/bin/
vagrant@vagrant:~$ PATH="/tmp/new_path_directory/bash:/usr/local/bin/:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
vagrant@vagrant:~$ type -a bash
bash is /usr/local/bin/bash
bash is /usr/bin/bash
bash is /bin/bash

```

13. Команда `at` позволяет запустить команду в определённое время, а команда `batch` - когда загрузка снизится до указанного уровня.. Вроде бы по man'у так, но как-то странно... ;)

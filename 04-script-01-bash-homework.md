***1. Есть скрипт:***

```
a=1
b=2
c=a+b
d=$a+$b
e=$(($a+$b))
```

Какие значения переменным c,d,e будут присвоены? Почему?

c = `a+b` - потому что тип переменной `c` - строка (определена неявно) и мы просто присвоили значение `a+b`
d = `1+2` - потому что тип переменной `c` - строка (определена неявно) и мы подставили значения переменных в этот текст и получилось `1+2`
e = `3` - потому что с помощью `$((...))` мы производим математические операции.

***2. На нашем локальном сервере упал сервис и мы написали скрипт, который постоянно проверяет его доступность, записывая дату проверок до тех пор, пока сервис не станет доступным. В скрипте допущена ошибка, из-за которой выполнение не может завершиться, при этом место на Жёстком Диске постоянно уменьшается. Что необходимо сделать, чтобы его исправить:***

```
while ((1==1)
do
curl https://localhost:4757
if (($? != 0))
then
date >> curl.log
fi
done

```

- во-первых, пропущена 2-я закрывающаяся скобка в строке `while`
- во-вторых, я бы сделал его немного другим:

```
while ((1==1))
do
curl https://localhost:4757
if (($? != 0))
then
date > curl.log
else
date > curl_ok.log
fi
done

```

Таким образом скрипт не будет загаживать место на диске и одновременно мы сможем посмотреть время последней удачной проверки.

***3. Необходимо написать скрипт, который проверяет доступность трёх IP: 192.168.0.1, 173.194.222.113, 87.250.250.242 по 80 порту и записывает результат в файл log. Проверять доступность необходимо пять раз для каждого узла.***

```
vagrant@vagrant:~$ cat check1.sh
#!/usr/bin/env bash
#set -euxo pipefail
#rm curl.log
ip_addresses=(192.168.0.1 173.194.222.113 87.250.250.242)
for ip in ${ip_addresses[@]}
do
        count=5
        while (($count > 0))
        do
                nc -zvw3 $ip 80 >> check_ip.log 2>&1
                let "count -= 1"
        done
done

vagrant@vagrant:~$ cat check_ip.log
nc: connect to 192.168.0.1 port 80 (tcp) timed out: Operation now in progress
nc: connect to 192.168.0.1 port 80 (tcp) timed out: Operation now in progress
nc: connect to 192.168.0.1 port 80 (tcp) timed out: Operation now in progress
nc: connect to 192.168.0.1 port 80 (tcp) timed out: Operation now in progress
nc: connect to 192.168.0.1 port 80 (tcp) timed out: Operation now in progress
Connection to 173.194.222.113 80 port [tcp/http] succeeded!
Connection to 173.194.222.113 80 port [tcp/http] succeeded!
Connection to 173.194.222.113 80 port [tcp/http] succeeded!
Connection to 173.194.222.113 80 port [tcp/http] succeeded!
Connection to 173.194.222.113 80 port [tcp/http] succeeded!
Connection to 87.250.250.242 80 port [tcp/http] succeeded!
Connection to 87.250.250.242 80 port [tcp/http] succeeded!
Connection to 87.250.250.242 80 port [tcp/http] succeeded!
Connection to 87.250.250.242 80 port [tcp/http] succeeded!
Connection to 87.250.250.242 80 port [tcp/http] succeeded!
```

***4. Необходимо дописать скрипт из предыдущего задания так, чтобы он выполнялся до тех пор, пока один из узлов не окажется недоступным. Если любой из узлов недоступен - IP этого узла пишется в файл error, скрипт прерывается***

```
vagrant@vagrant:~$ cat check2.sh
#!/usr/bin/env bash
#set -euxo pipefail
#rm curl.log
ip_addresses=(173.194.222.113 192.168.0.1 87.250.250.242)
for ip in ${ip_addresses[@]}
do
        count=5
        while (($count > 0))
        do
                nc -zvw3 $ip 80 >> check_ip.log 2>&1
                if (($? != 0))
                then
                        date > error.log
                        echo $ip >> error.log
                        break
                else
                        let "count -= 1"
                fi
        done
done


vagrant@vagrant:~$ cat error.log
Thu 13 Aug 2020 07:50:57 PM UTC
192.168.0.1

```

***5. Дополнительное задание (со звездочкой*) - необязательно к выполнению***
Мы хотим, чтобы у нас были красивые сообщения для коммитов в репозиторий. Для этого нужно написать локальный хук для git, который будет проверять, что сообщение в коммите содержит код текущего задания в квадратных скобках и количество символов в сообщении не превышает 30. Пример сообщения: [04-script-01-bash] сломал хук

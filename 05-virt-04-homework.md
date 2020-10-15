
***Задание 1.***

```
FROM archlinux:latest

RUN pacman -Suy --noconfirm && \
	pacman -S python3 coreutils texinfo unzip wget --noconfirm && \
	wget -O ponysay.zip http://github.com/erkin/ponysay/archive/master.zip && \
	unzip ponysay.zip && cd ponysay-master && \
	./setup.py install --freedom=partial && \
	pacman -R texinfo unzip wget --noconfirm && \
	rm -rf /ponysay.zip /ponysay-master /var/cache/pacman/pkg/*
	
ENTRYPOINT ["/usr/sbin/ponysay"]
CMD ["Hey, netology"]
```
Ссылка на репозиторий
https://hub.docker.com/repository/docker/avakhutinskiy/ponysay-vah


***Задание 2.***


*Dockerfile-j1*
```
FROM amazoncorretto:latest

RUN yum -y install wget && \
	wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo && \
	rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key && \
	yum -y upgrade && \
	yum -y install initscripts && \
	yum -y install jenkins java-1.8.0-openjdk-devel

CMD nohup java -jar /usr/lib/jenkins/jenkins.war > /var/log/jenkins/jenkins.log 2>&1
```

*Dockerfile-j2*

```
FROM ubuntu:latest
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get -y -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update && \
	apt-get -y install wget gnupg2 && \
	wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | apt-key add - && \
	echo "deb https://pkg.jenkins.io/debian-stable binary/" >> /etc/apt/sources.list && \
	apt-get -y -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update && \
	apt-get -y install jenkins openjdk-8-jdk

CMD nohup java -jar /usr/share/jenkins/jenkins.war > /var/log/jenkins/jenkins.log 2>&1
```

Скриншоты логов:
1-й контейнер
![](https://i.imgur.com/TbPxL3z.png)

![](https://i.imgur.com/7oTGUk7.png)
2-й контейнер
![](https://i.imgur.com/izgxepf.png)

![](https://i.imgur.com/EXD5WMl.png)

Скриншоты веб-интерфейсов:
1-й контейнер - порт 8080
![1-й контейнер](https://i.imgur.com/NQVyEjT.png)
2-й контейнер - порт 8081
![2-й контейнер](https://i.imgur.com/7KGK7QM.png)

```
docker tag jenkins1 avakhutinskiy/jenkins-vah:ver1
docker tag jenkins2 avakhutinskiy/jenkins-vah:ver2

docker push avakhutinskiy/jenkins-vah:ver1 ; docker push avakhutinskiy/jenkins-vah:ver2
```
Ссылка на репозиторий
https://hub.docker.com/repository/docker/avakhutinskiy/jenkins-vah

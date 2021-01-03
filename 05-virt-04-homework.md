
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

***Задание 3.***

Dockerfile

```
FROM node:latest

RUN git clone https://github.com/simplicitesoftware/nodejs-demo.git
WORKDIR "/nodejs-demo"
RUN	npm install
EXPOSE 3000
CMD ["npm", "start", "0.0.0.0"]
```

Вывод списка сетей
```
PS C:\Users\vah\docker\06-node> docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
048b5e31c23b        bridge              bridge              local
ec93bd5723cd        host                host                local
de8b9a9cdc8a        node_js_net         bridge              local
f43c80a849f4        none                null                local
```

Дополнение - вывод `inspect` сети
```
PS C:\Users\vah> docker network inspect node_js_net
[
    {
        "Name": "node_js_net",
        "Id": "de8b9a9cdc8a8bb6175143ea870808fed977ebabc106cb92e38b92c2bd64de70",
        "Created": "2020-10-15T04:58:13.3513261Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "552211eb3cac28784bbcc18662c6fdd11ae649bf5540d568c2d7164d97a3a551": {
                "Name": "ubuntu",
                "EndpointID": "674b50096e63c90376724af31f1cfaf9d3812eabf05dc3f9fb4f840f0ed329bc",
                "MacAddress": "02:42:ac:12:00:03",
                "IPv4Address": "172.18.0.3/16",
                "IPv6Address": ""
            },
            "5ee7bb82f3f9da18b9b47a524808728af106d9f309db4b207af2b245a04a34b6": {
                "Name": "node",
                "EndpointID": "02bffe1859c05427358cf5a27c3c7d7d0f012ae56f258a3ef393c44de674994e",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
```

Скриншот вывода curl'а

![Скриншот вывода curl'а](https://i.imgur.com/15GTmkm.png)

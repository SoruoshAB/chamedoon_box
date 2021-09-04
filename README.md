# Chamedoon box
django based api's
* this api service uses docker for deployment , make sure docker is installed, and it's running properly.
* make sure downloader service container is up
## Installation 
cd into chosen directory and clone the latest project
```bash
git clone http://gitlab.chamedon.me/Soroushi/box-backend.git
```
create a .env file just like sample.env

pull required docker images 

_Note: there are various docker images for each distribution these images are recommended for raspberry pi, ignore the arm tag if needed_
```bash
docker pull python:3.8
docker pull arm32v7/postgres:13-apline
docker pull arm32v7/redis:alpine
```
create volumes and networks
```bash
docker volume create box_postgres
docker volume create box_static
```

```bash
docker network create postgres_network
docker network create nginx_network
docker network create redis_network
```
cd into root of the project and run this command
```bash
docker-compose up -d
```
## Configuration
migrate and create superuser 
```bash
docker exec -it boxdjnago bash
```
``` bash
:/boxdjango# python manage.py makemigrations
:/boxdjango# python manage.py migrate
:/boxdjango# python manage.py createsuperuser
```



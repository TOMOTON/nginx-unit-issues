# Nginx Unit Issues

## Docker

### Build

```
$ cp .docker/.dockerignore .
$ sudo docker image build -f .docker/Dockerfile -t example/nginx-unit-issue:latest .
$ sudo docker run -i -t -p 8080:8080 --env-file /vagrant/DOCKER_ENV <image-id>
$ sudo docker run -i -t -p 8080:8080 --env-file /vagrant/DOCKER_ENV example/nginx-unit-issue:latest
```

## Run

```
sudo docker run -i -t -p 8080:8080 example/nginx-unit-issue:latest
```

sudo docker image build -f .docker/Dockerfile.3.8-alpine3.13 -t example/nginx-unit-issue .
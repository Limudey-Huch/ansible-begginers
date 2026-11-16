FROM geerlingguy/docker-ubuntu2204-ansible:latest

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y openssh-server \
 && systemctl enable ssh

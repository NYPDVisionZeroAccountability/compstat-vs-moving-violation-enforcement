#!/bin/bash

# Build go
cd /
git clone https://go.googlesource.com/go && cd go && git checkout go1.4.1 && cd src && CGO_ENABLED=1 ./make.bash
ln -s /go/bin/go /usr/sbin/go && ln -s /go/bin/gofmt /usr/sbin/gofmt


# Dummy docker
cd /
wget -qO- https://get.docker.io/gpg | sudo apt-key add - && sudo sh -c "echo deb http://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list" && sudo apt-get update && sudo apt-get install lxc-docker -y


# Build and Replace Docker
service docker stop
cd /
git clone https://github.com/docker/docker.git
cd docker
git checkout v1.7.0
AUTO_GOPATH=1 ./hack/make.sh dynbinary
cp /docker/bundles/1.7.0/dynbinary/dockerinit-1.7.0 /var/lib/docker/init/dockerinit
cp /docker/bundles/1.7.0/dynbinary/dockerinit-1.7.0 /usr/bin/dockerinit
cp /docker/bundles/1.7.0/dynbinary/docker-1.7.0 /usr/bin/docker
service docker start

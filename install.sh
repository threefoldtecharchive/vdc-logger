#!/bin/bash

apt-get update
apt-get install -y apt-transport-https
apt-get install -y software-properties-common wget
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
# Adding Grafana
echo "deb https://packages.grafana.com/oss/deb stable main" | tee -a /etc/apt/sources.list.d/grafana.list
apt-get update
apt-get install grafana -y

# Start Grafana
systemctl daemon-reload
systemctl start grafana-server
systemctl enable grafana-server.service

# Adding influx repo
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/lsb-release
echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | tee -a /etc/apt/sources.list.d/influxdb.list

apt-get update
apt-get install git python3-pip redis-server influxdb -y
sed -i 's/supervised no/supervised systemd/g' /etc/redis/redis.conf
sed -i 's/bind 127.0.0.1 ::1/bind 0.0.0.0 ::1/g' /etc/redis/redis.conf
systemctl restart redis.service
systemctl unmask influxdb.service
systemctl start influxdb

git clone --progress --verbose -b development_guni https://github.com/OmarElawady/vdc-logger.git

cd vdc-logger

# Update the Caddy service with the domain
sed -i "s/LOCAL_HOST/$1/g" Caddyfile

pip3 install -r requirements.txt

# Install Caddy server
echo "deb [trusted=yes] https://apt.fury.io/caddy/ /" \  | sudo tee -a /etc/apt/sources.list.d/caddy-fury.list

apt update
apt install caddy -y

systemctl stop caddy.service
systemctl disable caddy.service

# Create Influx database
influx -execute 'CREATE  DATABASE verify_keys'
influx -execute 'CREATE  DATABASE alerts'
influx -execute 'CREATE  DATABASE logs'

# Move our redis service to the systemd services
cp services/tf-redis-listener.service /etc/systemd/system
cp services/tf-logging-server.service /etc/systemd/system
cp services/tf-caddy-server.service /etc/systemd/system

# Reload and start the services
systemctl daemon-reload
systemctl start tf-redis-listener.service
systemctl start tf-logging-server.service
systemctl start tf-caddy-server.service
systemctl enable tf-redis-listener.service
systemctl enable tf-logging-server.service
systemctl enable tf-caddy-server.service

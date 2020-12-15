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
[[ -z "$REDISPASSWORD" ]] || sed -i "s/# requirepass foobared/requirepass $REDISPASSWORD/g" /etc/redis/redis.conf
[[ -z "$REDISPASSWORD" ]] || sed -i "s/REDIS_PASSWORD = None/REDIS_PASSWORD = \"$REDISPASSWORD\"/g" config.py
sed -i 's/bind 127.0.0.1 ::1/bind 0.0.0.0 ::1/g' /etc/redis/redis.conf
systemctl restart redis.service
systemctl unmask influxdb.service
systemctl start influxdb

git clone --progress --verbose -b main https://github.com/OmarElawady/vdc-logger.git

cd vdc-logger

# Add 3 orgs
devId=$(curl -X POST -H "Content-Type: application/json" -d '{"name":"devnet"}' http://admin:admin@localhost:3000/api/orgs | python3 -c "import sys, json; print(json.load(sys.stdin)['orgId'])")
testId=$(curl -X POST -H "Content-Type: application/json" -d '{"name":"testnet"}' http://admin:admin@localhost:3000/api/orgs | python3 -c "import sys, json; print(json.load(sys.stdin)['orgId'])")
mainId=$(curl -X POST -H "Content-Type: application/json" -d '{"name":"mainnet"}' http://admin:admin@localhost:3000/api/orgs | python3 -c "import sys, json; print(json.load(sys.stdin)['orgId'])")

curl -X POST http://admin:admin@localhost:3000/api/user/using/$devId
devtoken=$(curl -X POST -H 'Content-Type: application/json' -d '{"name":"devkey", "role": "Admin"}' -s 'http://admin:admin@localhost:3000/api/auth/keys' | python3 -c "import sys, json; print(json.load(sys.stdin)['key'])")

curl -X POST http://admin:admin@localhost:3000/api/user/using/$testId
testtoken=$(curl -X POST -H 'Content-Type: application/json' -d '{"name":"testkey", "role": "Admin"}' -s 'http://admin:admin@localhost:3000/api/auth/keys' | python3 -c "import sys, json; print(json.load(sys.stdin)['key'])")

curl -X POST http://admin:admin@localhost:3000/api/user/using/$mainId
maintoken=$(curl -X POST -H 'Content-Type: application/json' -d '{"name":"mainkey", "role": "Admin"}' -s 'http://admin:admin@localhost:3000/api/auth/keys' | python3 -c "import sys, json; print(json.load(sys.stdin)['key'])")

# Replace token if it is not found
count=$(cat logger/config.py | sed -n "/\GRAFANA_API_DEV_KEY/p" | wc -l)
if [ $count -gt 0 ]; then
    sed -i "s/GRAFANA_API_DEV_KEY/$devtoken/g" logger/config.py
fi

count=$(cat logger/config.py | sed -n "/\GRAFANA_API_TEST_KEY/p" | wc -l)
if [ $count -gt 0 ]; then
    sed -i "s/GRAFANA_API_TEST_KEY/$testtoken/g" logger/config.py
fi

count=$(cat logger/config.py | sed -n "/\GRAFANA_API_MAIN_KEY/p" | wc -l)
if [ $count -gt 0 ]; then
    sed -i "s/GRAFANA_API_MAIN_KEY/$maintoken/g" logger/config.py
fi

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
influx -execute 'CREATE  DATABASE heartbeats'

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

# Add Influx data source to Grafana data source
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $devtoken" -d '{"name":"InfluxDB","type":"influxdb","url":"http://localhost:8086","basicAuth":false,"message":"influx_db","access":"proxy","database":"logs","isDefault":true}' http://admin:admin@localhost:3000/api/datasources
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $testtoken" -d '{"name":"InfluxDB","type":"influxdb","url":"http://localhost:8086","basicAuth":false,"message":"influx_db","access":"proxy","database":"logs","isDefault":true}' http://admin:admin@localhost:3000/api/datasources
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $maintoken" -d '{"name":"InfluxDB","type":"influxdb","url":"http://localhost:8086","basicAuth":false,"message":"influx_db","access":"proxy","database":"logs","isDefault":true}' http://admin:admin@localhost:3000/api/datasources

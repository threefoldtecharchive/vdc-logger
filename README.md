### Introduction 
A monitoring solution for VDC's 3bots, provides:

- Monitoring 
    - Logs
    - Alerts 
    - Heartbeats

- Real time visualization using [Grafana](https://grafana.com/docs/grafana/latest/getting-started/getting-started/) 

This will help adminstration team to monitor the running 3bots for our clients


### Installation
- Get `install.sh` bash file and run 

```
sudo apt-get install curl -y

curl -Lo install.sh https://raw.githubusercontent.com/OmarElawady/vdc-logger/development_guni/install.sh  

bash install.sh <DOMAIN_NAME>
```

After running the previous command, you will get:

- [redis server](https://redis.io/)
- [influxdb](https://www.influxdata.com/)
- [Grafana server](https://grafana.com/docs/grafana/latest/getting-started/getting-started/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) running in production using [gunicorn](https://gunicorn.org/)
- `redislistener` process to get the logs
- [Caddy](https://caddyserver.com/) server to issue https certificate and serve our endpoints on `/api` and [Grafana](https://grafana.com/docs/grafana/latest/getting-started/getting-started/) server on `/`
- Our services running using `systemctl` service manager
    - `tf-caddy-server.service` responsible for running `Caddy`
    - `tf-loggin-server.service` responsible for running `gunicorn`
    - `tf-redis-listern.service` responsible for running `redislistener`

### After Installation
- `Grafana` will be available on: `<DOMAIN_NAME>`
- `API` endpoints will be available on: `<DOMAIN_NAME>/api/<END_POINT>`

#### Available endpoints
- `/api/register`
- `/api/heartbeat`
- `/api/alert`

### Enabling VDC 3bot monitoring 
Add these configurations to your 3bot

```python  
redis_config = {"channel_type":"redis","channel_host":"<DOMAIN_NAME>","channel_port":"6379"}                                                            
j.config.set("VDC_LOG_CONFIG",redis_config)    
j.config.set("MONITORING_SERVER_URL","https://<DOMAIN_NAME>/3bot/api/")
```
### Introduction 
A monitoring solution for VDC's 3bots, provides:

- Monitoring 
    - Logs
    - Alerts 
    - Heartbeats

- Real time visualization using [Grafana](https://grafana.com/docs/grafana/latest/getting-started/getting-started/) 

This will help adminstration team to monitor the running 3bots for our clients


### Installation

- Run 
`bash install.sh <DOMAIN_NAME>`

After running the previous command, you will get:

- [redis server](https://redis.io/)
- [influxdb](https://www.influxdata.com/)
- [Grafana server](https://grafana.com/docs/grafana/latest/getting-started/getting-started/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) running in production using [gunicorn](https://gunicorn.org/)
- `redislistener` process to get the logs
- [Caddy](https://caddyserver.com/) server to issue https certificate and serve our endpoints on `/api` and [Grafana](https://grafana.com/docs/grafana/latest/getting-started/getting-started/) server on `/`
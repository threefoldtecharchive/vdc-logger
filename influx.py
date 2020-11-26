from influxdb import InfluxDBClient

def connect_influx():
    # You can generate a Token from the "Tokens Tab" in the UI
    client = InfluxDBClient(host='localhost', port=8086, username='omar', password='omar')
    client.switch_database('logs')
    return client

def write_messages(client, points):
    client.write_points(points)
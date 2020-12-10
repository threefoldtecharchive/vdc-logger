import redis
from time import sleep
from influx import connect_influx, write_messages
import config


def process_message(message, db_connection):
    channel = message.get("channel").decode()
    message_data = message.get("data").decode()
    can = channel[4:]
    vdc_name, rest = can.split("_", 1)
    tname, stream = rest.rsplit("-", 1)
    points = [
        {
            "measurement": "logs",
            "tags": {"tname": tname, "vdc_name": vdc_name, "stream": stream},
            "fields": {"message": message_data},
        }
    ]
    write_messages(db_connection, points)


if __name__ == "__main__":
    db_connection = connect_influx()
    r = redis.Redis(host="localhost", port=int(config.REDIS_PORT), db=0)
    # r = redis.Redis(host="localhost", port=int(config.REDIS_PORT), password=config.REDIS_PASSWORD, db=0)

    p = r.pubsub()
    p.psubscribe("vdc_*_*-*")  # edit to match vdc only
    while True:
        x = p.get_message()
        while x:
            if x["type"] == "pmessage":
                process_message(x, db_connection)
                print(x)
            x = p.get_message()
        sleep(1)

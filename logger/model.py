from .db import get_db
from .exceptions import MissingValueException
import binascii

def insert_alert(json_data):
    # vdc_name, app_name, status, category, message, level, last_occurance
    client = get_db()
    client.switch_database('logs')
    tname = json_data.get('tname')
    explorer_url = json_data.get('explorer_url')
    level = json_data.get('level')
    vdc_name = json_data.get('vdc_name')
    app_name = json_data.get('app_name')
    status = json_data.get('status')
    category = json_data.get('category')
    type_ = json_data.get('type')
    count = json_data.get('count')
    message = json_data.get('message')
    if (
        tname is None or
        level is None or vdc_name is None or
        app_name is None or status is None or
        category is None or type_ is None or
        count is None or message is None
        ):
        raise MissingValueException("some properties are not provided")
    points = [
        {
            "measurement": "alerts",
            "tags": {
                "tname": tname,
                "explorer_url": explorer_url,
                "level": level,
                "vdc_name": vdc_name,
                "app_name": app_name,
                "status": status,
                "category": category,
                "type": type_,
            },
            "fields": {
                "message": message,
                "count": count,
            }
        },
    ]
    client.write_points(points)

def insert_heartbeat(json_data):
    client = get_db()
    client.switch_database('logs')
    tname = json_data.get('tname')
    explorer_url = json_data.get('explorer_url')
    vdc_name = json_data.get('vdc_name')
    if tname is None or vdc_name is None:
        raise MissingValueException("some properties are not provided")
    points = [
        {
            "measurement": "heartbeats",
            "tags": {
                "tname": tname,
                "explorer_url": explorer_url,
                "vdc_name": vdc_name
            },
            "fields": {
                "exists": 1
            }
        },
    ]
    client.write_points(points)

def get_verify_key_from_db(customer_tid, explorer_url):
    customer_tid = int(customer_tid)
    client = get_db()
    client.switch_database('keys')
    results = client.query('SELECT pubkey, tid, explorer_url FROM "keys"')
    vals = results.get_points(tags={'tid': str(customer_tid), 'explorer_url': explorer_url})
    try:
        key = next(vals)
        return binascii.unhexlify(key)
    except:
        return None

def cache_verify_key(customer_tid, explorer_url, verify_key):
    customer_tid = int(customer_tid)
    verify_key = binascii.hexlify(verify_key).decode()
    client = get_db()
    client.switch_database('keys')
    points = [
        {
            "measurement": "keys",
            "tags": {
                "tid": customer_tid,
                "explorer_url": explorer_url
            },
            "fields": {
                "pubkey": verify_key
            }
        },
    ]
    client.write_points(points)
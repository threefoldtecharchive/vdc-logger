from .db import get_db
from .exceptions import MissingValueException
import binascii
from flask import current_app
from .dashboard import get_dashboard_json
import json
import requests
from .utils import get_explorer_shortname


def insert_alert(json_data):
    # vdc_name, app_name, status, category, message, level, last_occurance
    client = get_db()
    client.switch_database("logs")
    tname = json_data.get("tname")
    explorer_url = json_data.get("explorer_url")
    level = json_data.get("level")
    vdc_name = json_data.get("vdc_name")
    app_name = json_data.get("app_name")
    status = json_data.get("status")
    category = json_data.get("category")
    type_ = json_data.get("type")
    count = json_data.get("count")
    message = json_data.get("message")
    if (
        tname is None
        or level is None
        or vdc_name is None
        or app_name is None
        or status is None
        or category is None
        or type_ is None
        or count is None
        or message is None
    ):
        raise MissingValueException("some properties are not provided")
    explorer = get_explorer_shortname(explorer_url)
    points = [
        {
            "measurement": "alerts",
            "tags": {
                "tname": tname,
                "explorer": explorer,
                "level": level,
                "vdc_name": vdc_name,
                "app_name": app_name,
                "status": status,
                "category": category,
                "type": type_,
            },
            "fields": {"message": message, "count": count},
        }
    ]
    client.write_points(points)


def insert_heartbeat(json_data):
    client = get_db()
    client.switch_database("logs")
    tname = json_data.get("tname")
    explorer_url = json_data.get("explorer_url")
    vdc_name = json_data.get("vdc_name")
    if tname is None or vdc_name is None:
        raise MissingValueException("some properties are not provided")
    explorer = get_explorer_shortname(explorer_url)
    points = [
        {
            "measurement": "heartbeats",
            "tags": {
                "tname": tname,
                "explorer": explorer,
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
    client.switch_database("verify_keys")
    results = client.query("SELECT pubkey, tid, explorer_url FROM verify_keys")
    vals = results.get_points(tags={"tid": str(customer_tid), "explorer_url": explorer_url})
    try:
        key = next(vals)
        return binascii.unhexlify(key)
    except:
        return None


def cache_verify_key(customer_tid, explorer_url, verify_key):
    customer_tid = int(customer_tid)
    verify_key = binascii.hexlify(verify_key).decode()
    client = get_db()
    client.switch_database("verify_keys")
    points = [
        {
            "measurement": "verify_keys",
            "tags": {"tid": customer_tid, "explorer_url": explorer_url},
            "fields": {"pubkey": verify_key},
        }
    ]
    client.write_points(points)


def add_new_dashboard(json_data):
    tname = json_data.get('tname')
    vdc_name = json_data.get('vdc_name')
    explorer_url = json_data.get('explorer_url')
    explorer = get_explorer_shortname(explorer_url)
    if tname is None or vdc_name is None or explorer_url is None:
        raise MissingValueException("some properties are not provided")
    token = current_app.config["GRAFANA_KEYS"][explorer]
    dashboard_str = get_dashboard_json(tname, vdc_name, explorer)
    hed = {'Authorization': 'Bearer ' + token}
    requests.post("http://localhost:3000/api/dashboards/db", json=json.loads(dashboard_str), headers=hed)

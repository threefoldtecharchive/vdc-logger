import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from influxdb import InfluxDBClient
from flask import current_app


def get_db():
    return InfluxDBClient(host=current_app.config['DB_HOST'], port=current_app.config['DB_PORT'], username=current_app.config['DB_USERNAME'], password=current_app.config['DB_PASSWORD'])

def close_db(e=None):
    g.pop('db', None)

def init_db():
    db_client = get_db()
    db_client.create_database("keys")
    db_client.create_database("alerts")
    db_client.create_database("logs")


def init_app(app):
    init_db()
    app.teardown_appcontext(close_db)


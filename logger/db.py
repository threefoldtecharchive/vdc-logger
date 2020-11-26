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
    pass

def init_app(app):
    app.teardown_appcontext(close_db)


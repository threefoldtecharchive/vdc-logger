import os
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    from . import db

    db.init_app(app)

    from . import logging

    app.register_blueprint(logging.bp)

    return app

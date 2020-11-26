import flask
from flask import Blueprint
from flask import Response
from flask import jsonify
from flask.templating import render_template
from .model import insert_heartbeat, insert_alert
from .db import get_db
from .helpers import validate_signature, get_verify_key, verify_request
from .exceptions import MissingValueException
from nacl.exceptions import BadSignatureError
import binascii

bp = Blueprint('logs', __name__)

@bp.route('/alert', methods=["POST"])
def alert():
    json_data = flask.request.json
    err, code = None, 200
    if json_data is None:
        err = {'error': "JSON data only allowed"}
        code = 400
    if err is not None:
        return jsonify(err), code
    try:
        verify_request(json_data)
    except MissingValueException as e:
        err = {'error': str(e)}
        code = 400
    except (BadSignatureError, binascii.Error):
        err = {'error': "Couldn't validate signature"}
        code = 400

    if err is not None:
        return jsonify(err), code
    try:
        insert_alert(json_data)
    except MissingValueException as e:
        err = {'error': str(e)}
        code = 400
    except Exception as e:
        err = {'error': str(e)}
        code = 500
    if err is not None:
        return jsonify(err), code
    result = {"success": True}
    return result, code


@bp.route('/heartbeat', methods=["POST"])
def heartbeat():
    json_data = flask.request.json
    err, code = None, 200
    if json_data is None:
        err = {'error': "JSON data only allowed"}
        code = 400
    if err is not None:
        return jsonify(err), code
    try:
        verify_request(json_data)
    except MissingValueException as e:
        err = {'error': str(e)}
        code = 400
    except (BadSignatureError, binascii.Error):
        err = {'error': "Couldn't validate signature"}
        code = 400
    if err is not None:
        return jsonify(err), code
    try:
        insert_heartbeat(json_data)
    except MissingValueException as e:
        err = {'error': str(e)}
        code = 400
    except Exception as e:
        err = {'error': str(e)}
        code = 500
    if err is not None:
        return jsonify(err), code
    result = {"success": True}
    return result, code

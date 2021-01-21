import flask
from flask import Blueprint
from flask import jsonify
from .model import insert_heartbeat, insert_alert, add_new_dashboard
from .helpers import verify_request
from .exceptions import MissingValueException, RegisteringDashboardException
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

@bp.route("/register", methods=["POST"])
def register():
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
        add_new_dashboard(json_data)
    except MissingValueException as e:
        err = {'error': str(e)}
        code = 400
    except RegisteringDashboardException as e:
        err = {'error': str(e)}
        code = 500
    except Exception as e:
        err = {'error': str(e)}
        code = 500
    if err is not None:
        return jsonify(err), code
    result = {"success": True}
    return result, code


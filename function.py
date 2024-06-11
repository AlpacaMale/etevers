from flask import redirect, session, g, jsonify
from models import db
from functools import wraps

def error(code):
    return jsonify({code: get_status_code(code)})

def get_status_code(code):
    status = {
        400: 'Bad Request',
        401: 'Unauthorized',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
    }
    return status.get(code)

def get_db():
    if 'db' not in g:
        g.db = db.session()
    return g.db

def teardown_request(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

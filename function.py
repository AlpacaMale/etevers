from flask import redirect, session, g, jsonify, current_app
from models import db
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps
from ping3 import ping
from config import DB_ROUTE, RDS_ROUTE


def error(code):
    return jsonify({code: get_status_code(code)})


def get_status_code(code):
    status = {
        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        502: "Bad Gateway",
        503: "Service Unavailable",
    }
    return status.get(code)


def get_db(bind_key):
    if not hasattr(g, f"{bind_key}_db"):
        engine = db.get_engine(current_app, bind=bind_key)
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        setattr(g, f"{bind_key}_db", Session)
    return getattr(g, f"{bind_key}_db")


def teardown_request(exception):
    for bind_key in ("db", "rds"):
        session = getattr(g, f"{bind_key}_db", None)
        if session is not None:
            session.remove()
            delattr(g, f"{bind_key}_db")


def get_primary_db():
    if ping(DB_ROUTE, timeout=0.1):
        return get_db("db")
    else:
        return get_db("rds")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

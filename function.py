from flask import redirect, session, g
from sqlalchemy.orm import scoped_session
from functools import wraps

def get_db(db_session: scoped_session):
    if 'db' not in g:
        g.db = db_session()
    return g.db

def teardown_request(exception, db_session: scoped_session):
    db = g.pop('db', None)
    if db is not None:
        db_session.remove()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

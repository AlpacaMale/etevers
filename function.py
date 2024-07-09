from flask import redirect, session, g, jsonify, current_app, request
from models import (
    db,
    MealPlanItem,
    MealPlanTracking,
    MealPreference,
    UserProfile,
)
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps
from ping3 import ping
from config import DB_PRIMARY_ROUTE, DB_SECONDARY_ROUTE, RDS_ROUTE
from ai import (
    create_meal_chain_1,
    create_meal_chain_2,
    create_meal_chain_3,
    create_meal_chain_4,
)
from datetime import date as dt_date
import json


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
        db_session = scoped_session(session_factory)
        setattr(g, f"{bind_key}_db", db_session)
    return getattr(g, f"{bind_key}_db")


def teardown_request(exception):
    for bind_key in ("db_primary", "db_secondary", "rds"):
        db_session = getattr(g, f"{bind_key}_db", None)
        if db_session is not None:
            db_session.remove()
            delattr(g, f"{bind_key}_db")


def get_primary_db():
    if ping(DB_PRIMARY_ROUTE, timeout=0.1):
        return get_db("db_primary")
    elif ping(DB_SECONDARY_ROUTE, timeout=0.1):
        return get_db("db_secondary")
    else:
        return get_db("rds")


def process_meal_plan(email, task_id):
    db = get_primary_db()
    today = dt_date.today()

    user_info = db.query(UserProfile).filter_by(users_email=email).first()
    preference_datas = db.query(MealPreference).filter_by(users_email=email).all()
    response1 = create_meal_chain_1(user_info, preference_datas)
    print(response1)
    response2 = create_meal_chain_2(response1)
    print(response2)
    response3 = create_meal_chain_3(response2)
    print(response3)
    try:
        meal_plan_items = json.loads(response3)
    except:
        response4 = create_meal_chain_4(response2)
        session[task_id]["status"] = "error"
        session[task_id]["error_msg"] = response4  # 에러 메시지를 딕셔너리에 저장
        return

    print(meal_plan_items)

    for meal_plan_item in meal_plan_items:
        new_meal_plan_item = MealPlanItem(
            users_email=email,
            starting_date=today,
            date=meal_plan_item.get("date"),
            meal_time=meal_plan_item.get("meal_type"),
            food_item=meal_plan_item.get("diet"),
        )
        db.add(new_meal_plan_item)
        db.commit()
        new_meal_plan_tracking = MealPlanTracking(
            meal_plan_items_id=new_meal_plan_item.id, status="yet"
        )
        db.add(new_meal_plan_tracking)
        db.commit()

    session[task_id] = {"status": "complete", "error_msg": None}


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") is None:
            # 사용자가 접근하려고 했던 URL을 세션에 저장
            session["next"] = request.url
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

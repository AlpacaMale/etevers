from flask import redirect, session, g, jsonify, current_app, request
import logging
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
    create_meal_chain_3,
    create_meal_chain_4,
)
from datetime import date as dt_date
import json


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


def process_meal_plan(app, email, task_id, tasks, tasks_lock):
    with app.app_context():
        logging.debug(f"Starting process_meal_plan for task_id: {task_id}")
        try:
            db = get_primary_db()
            today = dt_date.today()
            user_info = db.query(UserProfile).filter_by(users_email=email).first()
            preference_datas = (
                db.query(MealPreference).filter_by(users_email=email).all()
            )

            with tasks_lock:
                tasks[task_id] = {"status": "in-progress", "error_msg": None}

            response1 = create_meal_chain_1(user_info, preference_datas)
            logging.debug(f"Response1: {response1}")

            response2 = []
            try:
                loaded_responses = json.loads(response1)
                for loaded_response in loaded_responses:
                    date = loaded_response.get("date")
                    meal_type = loaded_response.get("meal_type")
                    diet_list = loaded_response.get("diet").split(" / ")
                    for diet in diet_list:
                        meal_plan_item = {
                            "date": date,
                            "meal_type": meal_type,
                            "diet": diet,
                        }
                        response2.append(meal_plan_item)

            except Exception as e:
                response4 = create_meal_chain_4(response1)
                with tasks_lock:
                    tasks[task_id] = {"status": "error", "error_msg": response4}
                return
            logging.debug(f"Response2: {response2}")

            response3 = create_meal_chain_3(response2)
            logging.debug(f"Response3: {response3}")

            try:
                meal_plan_items = json.loads(response3)
            except Exception as e:
                response4 = create_meal_chain_4(response2)
                with tasks_lock:
                    tasks[task_id]["status"] = "error"
                    tasks[task_id][
                        "error_msg"
                    ] = response4  # 에러 메시지를 딕셔너리에 저장
                logging.error(
                    f"Error in process_meal_plan for task_id: {task_id}, response4: {response4}, exception: {e}"
                )
                return

            logging.debug(f"Meal Plan Items: {meal_plan_items}")

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

            with tasks_lock:
                tasks[task_id] = {"status": "complete", "error_msg": None}
            logging.debug(f"Completed process_meal_plan for task_id: {task_id}")

        except Exception as e:
            with tasks_lock:
                tasks[task_id] = {"status": "error", "error_msg": str(e)}
            logging.error(
                f"Unexpected error in process_meal_plan for task_id: {task_id}, exception: {e}"
            )


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") is None:
            # 사용자가 접근하려고 했던 URL을 세션에 저장
            session["next"] = request.url
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

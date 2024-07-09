# webhook test
from flask import Flask, render_template, request, session, redirect, jsonify, send_file
from flask_session import Session
from datetime import date as dt_date, datetime
from config import Config
import threading
import time as t_time
from models import (
    db,
    time,
    sex,
    MealPlanItem,
    MealPlanTracking,
    MealPreference,
    User,
    UserProfile,
    WeightRecord,
    ChatbotInteraction,
)
from create import create_meal_plan_items
from sqlalchemy import asc, desc
from flask_sqlalchemy import SQLAlchemy
from graph import print_graph


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
Session(app)

thread_local = threading.local()
task_status = {}

from function import (
    login_required,
    get_primary_db,
    teardown_request,
    error,
    process_meal_plan,
)


@app.teardown_request
def teardown(exception):
    teardown_request(exception)


@app.route("/", methods=["GET", "POST"])
def get_started():
    if request.method == "POST":
        return redirect("/login")
    else:
        return render_template("get-started.html")


@app.route("/about-us", methods=["GET"])
def about_us():
    return render_template("about-us.html")


@app.route("/profile", methods=["GET"])
@login_required
def profile():
    db = get_primary_db()
    session["prev_page"] = "/profile"
    email = session.get("email")
    user_profile = db.query(UserProfile).filter_by(users_email=email).first()
    user_info = db.query(User.created_at).filter_by(email=email).first()[0]
    weight_datas = (
        db.query(WeightRecord)
        .filter_by(users_email=email)
        .order_by(asc(WeightRecord.date))
        .all()
    )
    preference_datas = db.query(MealPreference).filter_by(users_email=email).all()

    for weight_data in weight_datas:
        print(weight_data.users_email, weight_data.date, weight_data.weight)
    for preference_data in preference_datas:
        print(
            preference_data.food_item,
        )
    print(
        user_profile.users_email,
        user_profile.height,
        user_profile.weight,
        user_profile.sex,
        user_profile.dietary_belief,
        user_profile.exercise_frequency,
        user_info,
    )
    return render_template(
        "profile.html",
        user_profile=user_profile,
        user_info=user_info,
        weight_datas=weight_datas,
        preference_datas=preference_datas,
    )


@app.route("/edit-user-profile", methods=["GET", "POST"])
@login_required
def edit_user_profile():
    db = get_primary_db()
    email = session.get("email")
    user_profile = db.query(UserProfile).filter_by(users_email=email).first()

    if request.method == "POST":
        edit_user_data = request.form.to_dict()
        print(
            edit_user_data.get("height"),
            edit_user_data.get("weight"),
            edit_user_data.get("sex"),
            edit_user_data.get("dietary_belief"),
            edit_user_data.get("exercise_frequency"),
        )

        user_profile.height = edit_user_data.get("height")
        date = dt_date.today()

        weight_record = (
            db.query(WeightRecord).filter_by(users_email=email, date=date).first()
        )
        weight = edit_user_data.get("weight")

        if weight_record:
            weight_record.weight = weight
        else:
            new_weight = WeightRecord(users_email=email, weight=weight, date=date)
            db.add(new_weight)

        user_profile.weight = weight
        user_profile.sex = edit_user_data.get("sex")
        user_profile.dietary_belief = edit_user_data.get("dietary_belief")
        user_profile.exercise_frequency = edit_user_data.get("exercise_frequency")
        db.commit()

        return redirect("/profile")
    else:

        print(
            user_profile.users_email,
            user_profile.height,
            user_profile.weight,
            user_profile.sex,
            user_profile.dietary_belief,
            user_profile.exercise_frequency,
        )
        return render_template(
            "edit-user-profile.html", user_profile=user_profile, sex=sex
        )


@app.route("/deregister", methods=["GET", "POST"])
def deregister():
    if request.method == "POST":
        db = get_primary_db()
        email = session.get("email")
        user = db.query(User).filter_by(email=email).first()

        print(user)

        if user:
            db.query(ChatbotInteraction).filter_by(users_email=email).delete()
            meal_plan_items_ids = (
                db.query(MealPlanItem.id).filter_by(users_email=email).all()
            )
            for meal_plan_items_id in meal_plan_items_ids:
                db.query(MealPlanTracking).filter_by(
                    meal_plan_items_id=meal_plan_items_id[0]
                ).delete()
            db.query(MealPlanItem).filter_by(users_email=email).delete()
            db.query(MealPreference).filter_by(users_email=email).delete()
            db.query(UserProfile).filter_by(users_email=email).delete()
            db.query(WeightRecord).filter_by(users_email=email).delete()
            db.delete(user)
            db.commit()

        return redirect("/logout")
    else:
        return render_template("deregister.html")


@app.route("/input", methods=["GET", "POST"])
@login_required
def input():
    db = get_primary_db()
    if request.method == "POST":
        meal_plan_items = request.form.to_dict()
        print(meal_plan_items)

        new_meal_plan_items = MealPlanItem(
            date=meal_plan_items.get("date"),
            meal_time=meal_plan_items.get("time"),
            food_item=meal_plan_items.get("food"),
        )
        db.add(new_meal_plan_items)
        db.commit()

        return redirect("/main")

    else:
        if session.get("date") is None:
            date = dt_date.today()
        else:
            date = session.get("date")

        print(time)
        print(date)
        return render_template("input.html", time=time, date=date)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = get_primary_db()
        login_data = request.form.to_dict()
        email = login_data.get("email")
        password = login_data.get("password")

        if not db.query(User).filter_by(email=email, password=password).first():
            return error(401)

        session["email"] = email

        # 원래 가려고 했던 페이지를 세션에서 받아와서 리디렉션하는 로직
        next_url = session.pop("next", None)
        if next_url:
            return redirect(next_url)
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db = get_primary_db()
        register_data = request.form.to_dict()
        print(register_data)
        email = register_data.get("email")
        if db.query(User).filter_by(email=email).first():
            return error(400)

        password = register_data.get("password")
        password_confirm = register_data.get("password-confirm")

        if password != password_confirm:
            return error(400)

        new_user = User(email=email, password=password)
        db.add(new_user)
        # 회원가입 로직

        height = register_data.get("height")
        weight = register_data.get("weight")
        user_sex = register_data.get("sex")
        dietary_belief = register_data.get("dietary_belief")
        exercise_frequency = register_data.get("exercise_frequency")
        new_user_profile = UserProfile(
            height=height,
            weight=weight,
            sex=user_sex,
            dietary_belief=dietary_belief,
            exercise_frequency=exercise_frequency,
            users_email=email,
        )
        new_weight = WeightRecord(
            users_email=email, weight=weight, date=dt_date.today()
        )
        db.add(new_weight)
        db.add(new_user_profile)
        db.commit()

        return redirect("/")

    else:

        print(sex)
        return render_template("register.html", sex=sex)


@app.route("/view-weight-record", methods=["GET"])
@login_required
def view_weight_record():
    db = get_primary_db()
    session["prev_page"] = "/view-weight-record"
    email = session.get("email")

    user_profile = db.query(UserProfile).filter_by(users_email=email).first()

    return render_template("view-weight-record.html", user_profile=user_profile)


@app.route("/plot.png", methods=["GET"])
@login_required
def plot_png():
    email = session.get("email")
    db = get_primary_db()
    weight_datas = (
        db.query(WeightRecord)
        .filter_by(users_email=email)
        .order_by(asc(WeightRecord.date))
        .all()
    )

    user_data = {"dates": [], "weights": []}

    for weight_data in weight_datas:
        print(weight_data.users_email, weight_data.date, weight_data.weight)
        user_data["dates"].append(weight_data.date)
        user_data["weights"].append(weight_data.weight)

    img = print_graph(user_data)

    return send_file(img, mimetype="image/png")


@app.route("/write-weight-record", methods=["GET", "POST"])
@login_required
def write_weight_record():
    if request.method == "POST":
        db = get_primary_db()
        weight_data = request.form.to_dict()
        print(weight_data)
        email = session.get("email")
        weight = weight_data.get("weight")
        date = datetime.strptime(weight_data.get("date"), "%Y-%m-%d")

        user_profile = db.query(UserProfile).filter_by(users_email=email).first()
        weight_record = (
            db.query(WeightRecord).filter_by(users_email=email, date=date).first()
        )
        last_weight_record = (
            db.query(WeightRecord)
            .filter_by(users_email=email)
            .order_by(desc(WeightRecord.date))
            .first()
        )

        if (
            not last_weight_record
            or last_weight_record.date <= date
            or date == dt_date.today()
        ):
            user_profile.weight = weight
            print(weight)

        if weight_record:
            weight_record.weight = weight
        else:
            new_weight = WeightRecord(users_email=email, weight=weight, date=date)
            db.add(new_weight)

        db.commit()
        prev_page = session.pop("prev_page", None)

        if not prev_page:
            return redirect("/view-weight-record")

        return redirect(prev_page)

    else:
        date = dt_date.today()
        print(date)
        return render_template("write-weight-record.html", date=date)


@app.route("/view-meal-preference", methods=["GET"])
@login_required
def view_meal_preference():
    db = get_primary_db()
    session["prev_page"] = "/view-meal-preference"
    email = session.get("email")
    preference_datas = db.query(MealPreference).filter_by(users_email=email).all()
    user_profile = db.query(UserProfile).filter_by(users_email=email).first()

    for preference_data in preference_datas:
        print(
            preference_data.food_item,
        )

    return render_template(
        "view-meal-preference.html",
        preference_datas=preference_datas,
        user_profile=user_profile,
    )


@app.route("/write-meal-preference", methods=["GET", "POST"])
@login_required
def write_meal_preference():
    if request.method == "POST":
        db = get_primary_db()
        preference_data = request.form.to_dict()
        print(preference_data)
        email = session.get("email")
        food_item = preference_data.get("food_item")
        preference_data_id = preference_data.get("preference_data_id")

        if food_item:
            new_preference = MealPreference(
                users_email=email,
                food_item=food_item,
            )
            db.add(new_preference)
            db.commit()

            prev_page = session.pop("prev_page", None)

            if not prev_page:
                return redirect("/view-meal-preference")

            return redirect(prev_page)
        else:
            db.query(MealPreference).filter_by(id=preference_data_id).delete()
            db.commit()
            return redirect("/write-meal-preference")

    else:
        date = dt_date.today()
        email = session.get("email")
        db = get_primary_db()
        preference_datas = db.query(MealPreference).filter_by(users_email=email).all()
        user_profile = db.query(UserProfile).filter_by(users_email=email).first()

        for preference_data in preference_datas:
            print(
                preference_data,
            )

        print(date)
        return render_template(
            "write-meal-preference.html",
            date=date,
            preference_datas=preference_datas,
            user_profile=user_profile,
        )


@app.route("/make-meal-plan", methods=["GET", "POST"])
@login_required
def make_meal_plan():
    email = session.get("email")
    if request.method == "POST":
        task_id = str(t_time.time())  # 간단한 task ID 생성
        task_status[task_id] = {"status": "in-progress", "error_msg": None}

        # 백그라운드 작업 실행
        threading.Thread(target=process_meal_plan, args=(email, task_id, app)).start()

        return render_template("loading.html", task_id=task_id)

    else:
        db = get_primary_db()
        email = session.get("email")
        user_profile = db.query(UserProfile).filter_by(users_email=email).first()
        preference_foods = (
            db.query(MealPreference.food_item).filter_by(users_email=email).all()
        )
        preference_foods = ", ".join(food[0] for food in preference_foods)

        print(
            user_profile.users_email,
            user_profile.height,
            user_profile.weight,
            user_profile.sex,
            user_profile.dietary_belief,
            user_profile.exercise_frequency,
        )
        print(preference_foods)
        return render_template(
            "make-meal-plan.html",
            user_profile=user_profile,
            preference_foods=preference_foods,
        )


@app.route("/main", methods=["GET", "POST"])
@login_required
def main():
    if request.method == "POST":
        session["date"] = request.form.get("date")
        print(session["date"])
        return redirect("/main")
    else:
        db = get_primary_db()
        email = session.get("email")

        if session.get("date") is None:
            date = dt_date.today()
            session["date"] = date.strftime("%Y-%m-%d")
            print(session["date"])

        else:
            print(type(session.get("date")))
            date = datetime.strptime(session.get("date"), "%Y-%m-%d").date()
            print(type(date))

        meal_plan_items = (
            db.query(MealPlanItem).filter_by(users_email=email, date=date).all()
        )

        for meal_plan_item in meal_plan_items:
            print(
                meal_plan_item.date, meal_plan_item.meal_time, meal_plan_item.food_item
            )

        user_meal_data = {}
        user_missed_meal_datas = []
        for meal_plan_item in meal_plan_items:

            meal_plan_track = (
                db.query(MealPlanTracking)
                .filter_by(meal_plan_items_id=meal_plan_item.id)
                .first()
            )
            print(meal_plan_track)

            if meal_plan_track.status == "missed":
                user_missed_meal_datas.append(
                    [
                        meal_plan_item.meal_time,
                        meal_plan_item.food_item,
                        meal_plan_item.id,
                    ]
                )
            else:
                if user_meal_data.get(meal_plan_item.meal_time) is None:
                    user_meal_data[meal_plan_item.meal_time] = [
                        {meal_plan_item.food_item: meal_plan_item.id}
                    ]
                else:
                    user_meal_data[meal_plan_item.meal_time].append(
                        {meal_plan_item.food_item: meal_plan_item.id}
                    )

        print(user_meal_data)
        print(date)
        return render_template(
            "main.html",
            user_meal_data=user_meal_data,
            date=date,
            user_missed_meal_datas=user_missed_meal_datas,
        )


@app.route("/edit-meal", methods=["GET", "POST"])
@login_required
def edit_meal():
    db = get_primary_db()
    if request.method == "POST":
        meal_data = request.form.to_dict()

        print(meal_data)

        missed_meal_id = meal_data.get("missed_meal_id")
        completed_meal_id = meal_data.get("completed_meal_id")
        meal_time = meal_data.get("meal_time")
        food_item = meal_data.get("food_item")
        session["tab"] = meal_data.get("tab")
        if meal_data.get("date"):
            date = meal_data.get("date")
            session["date"] = date
            print(session["date"])

            return redirect("/edit-meal")
        else:
            date = datetime.strptime(session.get("date"), "%Y-%m-%d").date()
        starting_date = datetime.strptime(
            session.get("starting_date"), "%Y-%m-%d"
        ).date()
        email = session.get("email")

        print(type(session.get("date")))

        if missed_meal_id:
            meal_plan_track = (
                db.query(MealPlanTracking)
                .filter_by(meal_plan_items_id=missed_meal_id)
                .first()
            )
            meal_plan_track.status = "missed"
            db.commit()
        elif completed_meal_id:
            meal_plan_track = (
                db.query(MealPlanTracking)
                .filter_by(meal_plan_items_id=completed_meal_id)
                .first()
            )
            meal_plan_track.status = "completed"
            db.commit()
        else:
            new_meal_plan_item = MealPlanItem(
                users_email=email,
                starting_date=starting_date,
                date=date,
                meal_time=meal_time,
                food_item=food_item,
            )
            db.add(new_meal_plan_item)
            db.commit()
            new_meal_plan_tracking = MealPlanTracking(
                meal_plan_items_id=new_meal_plan_item.id, status="completed"
            )
            db.add(new_meal_plan_tracking)
            db.commit()

        return redirect("/edit-meal")
    else:
        email = session.get("email")
        date = datetime.strptime(session.get("date"), "%Y-%m-%d").date()
        tab = session.pop("tab", "breakfast")

        meal_plan_items = (
            db.query(MealPlanItem).filter_by(users_email=email, date=date).all()
        )

        if meal_plan_items:
            session["starting_date"] = meal_plan_items[0].starting_date.strftime(
                "%Y-%m-%d"
            )

        for meal_plan_item in meal_plan_items:
            print(
                meal_plan_item.date, meal_plan_item.meal_time, meal_plan_item.food_item
            )

        user_meal_data = {}
        user_missed_meal_datas = {}
        for meal_plan_item in meal_plan_items:

            meal_plan_track = (
                db.query(MealPlanTracking)
                .filter_by(meal_plan_items_id=meal_plan_item.id)
                .first()
            )
            print(meal_plan_track)

            if meal_plan_track.status == "missed":
                if user_missed_meal_datas.get(meal_plan_item.meal_time) is None:
                    user_missed_meal_datas[meal_plan_item.meal_time] = [
                        {meal_plan_item.food_item: meal_plan_item.id}
                    ]
                else:
                    user_missed_meal_datas[meal_plan_item.meal_time].append(
                        {meal_plan_item.food_item: meal_plan_item.id}
                    )
            else:
                if user_meal_data.get(meal_plan_item.meal_time) is None:
                    user_meal_data[meal_plan_item.meal_time] = [
                        {meal_plan_item.food_item: meal_plan_item.id}
                    ]
                else:
                    user_meal_data[meal_plan_item.meal_time].append(
                        {meal_plan_item.food_item: meal_plan_item.id}
                    )

        print(user_meal_data)
        return render_template(
            "edit-meal.html",
            user_meal_data=user_meal_data,
            date=date,
            user_missed_meal_datas=user_missed_meal_datas,
            time=time,
            tab=tab,
        )


@app.route("/error/<task_id>")
def error(task_id):
    error_msg = task_status.get(
        task_id, {"status": "not-found", "error_msg": None}
    ).get("error_msg")
    return render_template("error.html", error_msg=error_msg)


@app.route("/task-status/<task_id>")
def task_status_check(task_id):
    status_info = task_status.get(task_id, {"status": "not-found", "error_msg": None})
    print(status_info)
    return jsonify(status_info)


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

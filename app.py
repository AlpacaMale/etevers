# webhook test
from flask import Flask, render_template, request, session, redirect, jsonify
from function import login_required, get_db, teardown_request, error
from datetime import date as dt_date, timedelta, datetime
from config import Config
from models import db, time, sex, MealPlanItem, MealPlanTracking, MealPreference, User, UserProfile, WeightRecord, ChatbotInteraction
from create import create_meal_plan_items
from sqlalchemy import asc, desc

# from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_request
def before_request():
    get_db()

@app.teardown_request
def teardown(exception):
    teardown_request(exception)

@app.route("/", methods=["GET","POST"])
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
    db = get_db()
    email = session.get("email")
    user_profile = db.query(UserProfile).filter_by(users_email=email).first()
    user_info = db.query(User.created_at).filter_by(email=email).first()[0]
    weight_datas = db.query(WeightRecord).filter_by(users_email=email).order_by(asc(WeightRecord.date)).all()
    preference_datas = db.query(MealPreference).filter_by(users_email=email).all()

    for weight_data in weight_datas:
        print(weight_data.users_email, weight_data.date, weight_data.weight)
    for preference_data in preference_datas:
        print(preference_data.food_item, preference_data.frequency_min, preference_data.frequency_max)
    print(user_profile.users_email, user_profile.height, user_profile.weight, user_profile.sex, user_profile.dietary_belief, user_profile.exercise_frequency, user_info)
    return render_template("profile.html", user_profile=user_profile, user_info=user_info, weight_datas=weight_datas, preference_datas=preference_datas)

@app.route("/edit-user-profile", methods=["GET", "POST"])
@login_required
def edit_user_profile():
    db = get_db()
    email = session.get("email")
    user_profile = db.query(UserProfile).filter_by(users_email=email).first()
    
    if request.method == "POST":
        edit_user_data = request.form.to_dict()
        print(edit_user_data.get('height'), edit_user_data.get('weight'), edit_user_data.get('sex'), edit_user_data.get('dietary_belief'), edit_user_data.get('exercise_frequency'))

        user_profile.height = edit_user_data.get("height")
        date = dt_date.today()

        weight_record = db.query(WeightRecord).filter_by(users_email=email, date=date).first()
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
        
        print(user_profile.users_email, user_profile.height, user_profile.weight, user_profile.sex, user_profile.dietary_belief, user_profile.exercise_frequency)
        return render_template("edit-user-profile.html", user_profile=user_profile, sex=sex)

@app.route("/deregister", methods=["GET", "POST"])
def deregister():
    if request.method == "POST":
        db = get_db()
        email = session.get("email")
        user = db.query(User).filter_by(email=email).first()

        print(user)

        if user:
            db.query(ChatbotInteraction).filter_by(users_email=email).delete()
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
    db = get_db()
    if request.method == "POST":
        meal_plan_items = request.form.to_dict()
        print(meal_plan_items)
        
        new_meal_plan_items = MealPlanItem(date=meal_plan_items.get('date'), meal_time=meal_plan_items.get('time'),food_item=meal_plan_items.get('food'))
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
        db = get_db()
        login_data = request.form.to_dict()
        email = login_data.get("email")
        password = login_data.get("password")

        if not db.query(User).filter_by(email=email, password=password).first():
            return error(401)
        
        session['email'] = email
        
        return redirect("/main")
        
        #원래 가려고 했던 페이지를 세션에서 받아와서 리디렉션하는 로직

    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        db = get_db()
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
        new_user_profile = UserProfile(height=height, weight=weight, sex=user_sex, dietary_belief=dietary_belief, exercise_frequency=exercise_frequency, users_email=email)
        db.add(new_user_profile)
        db.commit()
        
        return redirect("/")

    else:

        print(sex)
        return render_template("register.html" , sex=sex)

@app.route("/view-weight-record", methods=["GET"])
@login_required
def view_weight_record():
    email = session.get("email")
    db = get_db()
    weight_datas = db.query(WeightRecord).filter_by(users_email=email).order_by(asc(WeightRecord.date)).all()
    user_profile = db.query(UserProfile).filter_by(users_email=email).first()
    
    for weight_data in weight_datas:
        print(weight_data.users_email, weight_data.date, weight_data.weight)
    

    return render_template("view-weight-record.html", weight_datas=weight_datas, user_profile=user_profile)

@app.route("/write-weight-record", methods=["GET","POST"])
@login_required
def write_weight_record():
    if request.method == "POST":
        db = get_db()
        weight_data = request.form.to_dict()
        print(weight_data)
        email = session.get("email")
        weight = weight_data.get('weight')
        date = datetime.strptime(weight_data.get('date'), "%Y-%m-%d")

        user_profile = db.query(UserProfile).filter_by(users_email=email).first()
        weight_record = db.query(WeightRecord).filter_by(users_email=email, date=date).first()
        last_weight_record = db.query(WeightRecord).filter_by(users_email=email).order_by(desc(WeightRecord.date)).first()

        if not last_weight_record or last_weight_record.date <= date and date == dt_date.today():
            user_profile.weight = weight

        if weight_record:
            weight_record.weight = weight
        else:
            new_weight = WeightRecord(users_email=email, weight=weight, date=date)
            db.add(new_weight)

        db.commit()
        
        return redirect("/view-weight-record")

    else:
        date = dt_date.today()
        print(date)
        return render_template("write-weight-record.html", date=date)
    
@app.route("/view-meal-preference", methods=["GET"])
@login_required
def view_meal_preference():
    db = get_db()
    email = session.get("email")
    preference_datas = db.query(MealPreference).filter_by(users_email=email).all()
    user_profile = db.query(UserProfile).filter_by(users_email=email).first()

    for preference_data in preference_datas:
        print(preference_data.food_item, preference_data.frequency_min, preference_data.frequency_max)
    
    return render_template("view-meal-preference.html", preference_datas=preference_datas, user_profile=user_profile)

@app.route("/write-meal-preference", methods=["GET","POST"])
@login_required
def write_meal_preference():
    if request.method == "POST":
        db = get_db()
        preference_data_data = request.form.to_dict()
        print(preference_data_data)
        email = session.get("email")
        food_item = preference_data_data.get('food_item')
        frequency_min = preference_data_data.get('frequency_min')
        frequency_max = preference_data_data.get('frequency_max')
        
        new_preference = MealPreference(users_email=email, food_item=food_item, frequency_min=frequency_min, frequency_max=frequency_max)
        db.add(new_preference)
        db.commit()
        
        return redirect("/view-meal-preference")

    else:
        date = dt_date.today()

        print(date)
        return render_template("write-meal-preference.html", date=date)

@app.route("/make-meal-plan", methods=["GET", "POST"])
@login_required
def make_meal_plan():
    db = get_db()
    if request.method == "POST":
        email = session.get("email")
        today = dt_date.today()

        meal_plan_items = create_meal_plan_items(dt_date.today())
        for meal_plan_item in meal_plan_items:
            new_meal_plan_item = MealPlanItem(users_email=email,starting_date=today, date=meal_plan_item.get('date'), meal_time=meal_plan_item.get('meal_time'), food_item=meal_plan_item.get('food_item'))
            db.add(new_meal_plan_item)
            
        db.commit()
        return redirect("/main")
    
    else:
        email = session.get("email")
        user_profile = db.query(UserProfile).filter_by(users_email=email).first()
        preference_foods = db.query(MealPreference.food_item).filter_by(users_email=email).all()
        preference_foods = [food[0] for food in preference_foods]
        print(user_profile.users_email, user_profile.height, user_profile.weight, user_profile.sex, user_profile.dietary_belief, user_profile.exercise_frequency)
        print(preference_foods)
        return render_template("make-meal-plan.html", user_profile=user_profile, preference_foods=preference_foods)
    
@app.route("/main", methods=["GET","POST"])
@login_required
def main():
    if request.method == "POST":
        session['date'] = datetime.strptime(request.form.get("date"), "%Y-%m-%d")
        return redirect("/main")
    else:
        db = get_db()
        email = session.get("email")

        if session.get("date") is None:
            date = dt_date.today()
        else:
            date = session.get("date")

        meal_plan_items = db.query(MealPlanItem).filter_by(users_email=email, date=date).all()

        for meal_plan_item in meal_plan_items:
            print(meal_plan_item.date, meal_plan_item.meal_time, meal_plan_item.food_item)

        user_meal_data = {}
        for meal_plan_item in meal_plan_items:
            if user_meal_data.get(meal_plan_item.meal_time) is None:
                user_meal_data[meal_plan_item.meal_time] = [meal_plan_item.food_item]
            else:
                user_meal_data[meal_plan_item.meal_time].append(meal_plan_item.food_item)
        
        print(user_meal_data)
        print(date)
        return render_template("main.html", user_meal_data=user_meal_data, date=date)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200
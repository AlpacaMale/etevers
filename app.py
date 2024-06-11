# webhook test
from flask import Flask, render_template, request, session, redirect, jsonify
from function import login_required, get_db, teardown_request, error
from datetime import date as dt_date, timedelta
from config import Config
from models import db, time, sex, MealPlan, MealPlanItem, MealPlanTracking, MealPreference, User, UserProfile, WeightRecord
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

@app.route("/week", methods=["GET"])
def week():
    #로그인 필요
    #음식 업로드
    #AI과 통신
    return render_template("week.html")

@app.route("/daily", methods=["GET"])
def daily():
    #로그인 필요
    #음식 업로드
    #AI과 통신
    return render_template("daily.html")

@app.route("/profile", methods=["GET"])
def profile():
    #로그인 필요
    #회원 탈퇴
    #비밀번호 변경
    return render_template("profile.html")

@app.route("/password-check", methods=["GET"])
def password_check():
    #비밀번호 확인하는 로직
    return render_template("password-check.html")

@app.route("/deregister", methods=["GET"])
def deregister():
    #회원탈퇴 로직
    return render_template("deregister.html")

@app.route("/change-password", methods=["GET"])
def change_password():
    #비밀번호 변경 로직
    return render_template("change-password.html")

@app.route("/input", methods=["GET", "POST"])
@login_required
def input():
    db = get_db()
    if request.method == "POST":
        meal_plan_items = request.form.to_dict()
        print(meal_plan_items)
        

        # 음식의 양에 대한 레코드가 추가되어야함
        new_meal_plan_items = MealPlanItem(date=meal_plan_items.get('date'), meal_time=meal_plan_items.get('time'),food_item=meal_plan_items.get('food'))
        db.add(new_meal_plan_items)
        db.commit()
        
        # 밀 플랜을 받아서 meal plan item 테이블에 쓰기
        return redirect("/main")
    else:
        if session.get("date") is None:
            date = dt_date.today().strftime("%Y-%m-%d")
        else:
            date = session.get("date")
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
        return render_template("register.html" , sex=sex)

@app.route("/view-weight-record", methods=["GET"])
@login_required
def view_weight_record():
    email = session.get("email")
    db = get_db()
    weight_datas = db.query(WeightRecord).filter_by(users_email=email).order_by(asc(WeightRecord.date)).all()
    for weight_data in weight_datas:
        print(weight_data.users_email, weight_data.date, weight_data.weight)
    return render_template("view-weight-record.html", weight_datas=weight_datas)

@app.route("/write-weight-record", methods=["GET","POST"])
@login_required
def write_weight_record():
    if request.method == "POST":
        db = get_db()
        weight_data = request.form.to_dict()
        print(weight_data)
        email = session.get("email")
        weight = weight_data.get('weight')
        date = weight_data.get('date')
        
        new_weight = WeightRecord(users_email=email, weight=weight, date=date)
        db.add(new_weight)
        db.commit()
        
        return redirect("/view-weight-record")

    else:
        date = dt_date.today().strftime("%Y-%m-%d")
        return render_template("write-weight-record.html", date=date)
    
@app.route("/view-meal-preference", methods=["GET"])
@login_required
def view_meal_preference():
    email = session.get("email")
    db = get_db()
    preference_datas = db.query(MealPreference).filter_by(users_email=email).all()
    for preference_data in preference_datas:
        print(preference_data.food_item, preference_data.frequency_min, preference_data.frequency_max)
    return render_template("view-meal-preference.html", preference_datas=preference_datas)

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
        date = dt_date.today().strftime("%Y-%m-%d")
        return render_template("write-meal-preference.html", date=date)

@app.route("/make-meal-plan", methods=["GET"])
@login_required
def make_meal_plan():
    db = get_db()
    email = session.get("email")
    meal_plan_start_date = db.query(MealPlan).filter_by(users_email=email).order_by(desc(MealPlan.created_at)).first().start_date
    if not meal_plan_start_date or dt_date.today() - dt_date.strptime(meal_plan_start_date.start_date, "%Y-%m-%d") > timedelta(days=7):
        new_meal_plan = MealPlan(users_email=email, start_date=dt_date.today().strftime("%Y-%m-%d"))
        db.add(new_meal_plan)
        db.commit()

        meal_plan_id = db.query(MealPlan).filter_by(users_email=email).order_by(desc(MealPlan.created_at)).first().id

        for day in range(0, 6):
            date = dt_date.today()+timedelta(days=day)
            date = date.strftime("%Y-%m-%d")
            new_meal_plan_item = MealPlanItem(users_email=email, id=meal_plan_id, date=date, meal_time='lunch', food_item='potato 150gram')
            db.add(new_meal_plan_item)
            db.commit()

    return redirect("/")
    
@app.route("/main", methods=["GET","POST"])
@login_required
def main():
    if request.method == "POST":
        session['date'] = request.form.get("date")
        return redirect("/main")
    else:
        email = session.get("email")
        meal_plan = db.query(MealPlan).filter_by(users_email=email).order_by(desc(MealPlan.created_at)).first()
        if not meal_plan or dt_date.today() - dt_date.strptime(meal_plan.start_date, "%Y-%m-%d") > timedelta(days=7):
            return redirect("/make-meal-plan")
        
        if session.get("date") is None:
            date = dt_date.today().strftime("%Y-%m-%d")
        else:
            date = session.get("date")

        user_meal_plan = []
        # 유저 밀플랜을 받아서 
        print(user_meal_plan)

        time = []
        # 타임별로(아침점심저녁)분류해서 프론트에 쏴줄데이터를 완성하는 로직
        print(time)

        user_meal_data = {}
        for user_meal_plan_row in user_meal_plan:
            if user_meal_plan_row.get("time") not in user_meal_data:
                user_meal_data[user_meal_plan_row.get("time")] = [user_meal_plan_row.get("food") + " " + user_meal_plan_row.get("amount")]
            else:
                user_meal_data[user_meal_plan_row.get("time")].append(user_meal_plan_row.get("food") + " " + user_meal_plan_row.get("amount"))
        print(user_meal_data)

        return render_template("main.html", user_meal_data=user_meal_data,date=date)

@app.route('/contents/aws')
def health():
    return jsonify({'status': 'ok'}), 200
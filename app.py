from flask import Flask, render_template, request, session, redirect, jsonify
from function import login_required, get_db, teardown_request, error
from datetime import date as dt_date
from config import Config
from models import db, time, MealPlan, MealPlanItem, MealPlanTracking, MealPreference, User, UserProfile, Weight

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
        meal_plan = request.form.to_dict()
        print(meal_plan)

        # 음식의 양에 대한 레코드가 추가되어야함
        new_meal_plan = MealPlanItem(date=meal_plan.get('date'), meal_time=meal_plan.get('time'),food_item=meal_plan.get('food'))
        db.add(new_meal_plan)
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
        email = register_data.get("email")
        if db.query(User).filter_by(email=email).first():
            return error(400)

        password = register_data.get("password")
        password_confirm = register_data.get("password-confirm")

        if password != password_confirm:
            return error(400)
        
        new_user = User(email=email, password=password)
        db.add(new_user)
        db.commit()
        # 회원가입 로직
        
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/main", methods=["GET","POST"])
@login_required
def main():
    if request.method == "POST":
        session['date'] = request.form.get("date")
        return redirect("/main")
    else:
        if session.get("date") is None:
            date = dt_date.today().strftime("%Y-%m-%d")
        else:
            date = session.get("date")
        email = session.get("email")

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
from flask import Flask, render_template, request, session, redirect, jsonify
from function import login_required, get_db, teardown_request
import datetime

##############sql######################
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# 데이터베이스 연결 URL을 설정합니다.
# 형식: 'mysql+pymysql://<username>:<password>@<host>/<dbname>'

DATABASE_URL = 'mysql+pymysql://user1:root@localhost/mydb'

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL)
db_session = scoped_session(sessionmaker(bind=engine))
#######################################

# from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.before_request
def before_request():
    get_db(db_session)

@app.teardown_request
def teardown(exception):
    teardown_request(exception, db_session)

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
    if request.method == "POST":
        meal_plan = request.form.to_dict()
        print(meal_plan)
        
        mid = 1
        with open(meal_plan_file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                mid = mid + 1

        email = session.get("email")
        new_row = [str(mid), email, meal_plan['date'], meal_plan['time'],meal_plan['food'],meal_plan['amount']]
        with open(meal_plan_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_row)
        return redirect("/main")
    else:
        if session.get("date") is None:
            date = datetime.date.today().strftime("%Y-%m-%d")
        else:
            date = session.get("date")
        email = session.get("email")
        time = []
        with open(time_file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    time+=row
        return render_template("input.html",email=email, time=time, date=date)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        login_data = request.form.to_dict()
        email = login_data.get("email")
        password = login_data.get("password")


        user_found = False
        with open(user_data_file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
    
        # 각 행을 순회하며 조건에 맞는 행 찾기
            for row in reader:
                if row['email'] == email and row["password"] == password:
                    user_found = True
                    session['email'] = email
                    break
        
        if user_found == True:
            return redirect("/main")
        else:
            return redirect("/login")
        
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
        register_data = request.form.to_dict()
        email = register_data.get("email")
        
        uid = 1
        with open(user_data_file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("email") == email:
                    return redirect("/register")
                uid = uid + 1
                
        password = register_data.get("password")
        password_confirm = register_data.get("password-confirm")

        if password != password_confirm:
            return redirect("/register")

        new_row = [ str(uid), email, password]
        with open(user_data_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_row)
        
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
            date = datetime.date.today().strftime("%Y-%m-%d")
        else:
            date = session.get("date")
        email = session.get("email")

        user_meal_plan = []
        with open(meal_plan_file_path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get("email") == email and row.get("date") == date:
                        user_meal_plan.append(row)
        print(user_meal_plan)

        time = []
        with open(time_file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    time += row
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
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps


app = Flask(__name__)

app.config["SECRET_KEY"] = "ProjectBuiltByTeamTerminators"


# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Login Manager

login_manager = LoginManager()
login_manager.init_app(app)

class Student(UserMixin, db.Model):
    __tablename__ = "students"
    sid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=False, nullable=False)
    password = db.Column(db.Text, nullable=False)
    mobile = db.Column(db.Text, nullable=True)
    course = db.Column(db.Text, nullable=True)
    branch = db.Column(db.Text, nullable=True)
    father_name = db.Column(db.Text, nullable=True)
    caste = db.Column(db.Text, nullable=True)
    eamcet_rank = db.Column(db.Text, nullable=True)
    bank = db.Column(db.Text, nullable=True)
    aadhar = db.Column(db.Text, nullable=True)
    ration_card = db.Column(db.Text, nullable=True)
    address = db.Column(db.Text, nullable=True)
    father_name = db.Column(db.Text, nullable=True)
    mother_name = db.Column(db.Text, nullable=True)
    father_mobile = db.Column(db.Text, nullable=True)
    mother_mobile = db.Column(db.Text, nullable=True)
    annual_income = db.Column(db.Text, nullable=True)
    father_mail = db.Column(db.Text, nullable=True)
    mother_mail = db.Column(db.Text, nullable=True)
    father_occupation = db.Column(db.Text, nullable=True)
    mother_occupation = db.Column(db.Text, nullable=True)
    profile = db.Column(db.Text, nullable=True)
    nationality = db.Column(db.Text, nullable=True)

class Employee(UserMixin, db.Model):
    __tablename__ = "employees"
    eid = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=False, nullable=False)
    password = db.Column(db.Text, unique=False)
    department = db.Column(db.Text, nullable=True)
    qualification = db.Column(db.Text, nullable=True)
    gender = db.Column(db.Text, nullable=True)

# class Subject(db.Model):
#     __tablename__ = "subjects"
#     sub_id = db.Column(db.Integer, primary_key=True)
#     sub_name = db.Column(db.Text, unique=True, nullable=False)
    
# class Notes(db.Model):
#     __tablename__ = "notes"
#     sub_id = db.Column(db.Integer, primary_key=True)
#     sub_name = db.Coumn(db.Text, unique=True, nullable=False)



# db.create_all()

def is_emp():
    if current_user.eid:
        return True
    else:
        return False

def emp_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if not is_emp():
                return abort(403)
            return f(*args, **kwargs)      
        except:
              return abort(403)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    try:
        return Student.query.get(user_id)
    except:
        return Employee.query.get(user_id)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/emp", methods=["POST"])
def emp():
    if request.method == "POST":
        email = request.form.get("email")
        user = Employee.query.filter_by(email=email).first()
        if user:
            password = request.form.get("password")
            if user.password == password:
                login_user(user)
                return redirect(url_for("home"))

            flash("Invalid password")
            return redirect(url_for("login"))

        flash("User not registered with email!")
        return redirect(url_for("login"))

    # return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route("/stu", methods=["POST"])
def stu():
    if request.method == "POST":
        email = request.form.get("email")
        user = Student.query.filter_by(email=email).form()
        if user:
            pwd = request.form.get("pwd")
            if user.password == pwd:
                login_user(user)
                return redirect(url_for("home"))
            flash("Invalid Password")
            return redirect(url_for("login"))
        flash("User not exists")
        return redirect(url_for("login"))
    
@app.route("/attendance")
def attendance():
    return render_template("attendance.html")

@app.route("/add_attendance")
def add_attendance():
    return render_template("add_attendance.html")
@app.route("/student_form")
def student_form():
    return render_template("student_form.html")
@app.route("/employee_form")
def employee_form():
    return render_template("employee_form.html")



@app.route("/add-student")
def add_student():
    return ""

@app.route("/logout")
def logout():
    logout_user(current_user)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)
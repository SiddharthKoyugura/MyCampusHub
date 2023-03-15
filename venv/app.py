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

class Student(UserMixin, db.Model):
    __tablename__ = "students"
    sid = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=False, nullable=False)
    password = db.Column(db.Text, nullable=False)

class Employee(UserMixin, db.Model):
    __tablename__ = "employees"
    eid = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=False, nullable=False)
    password = db.Column(db.Text, unique=False)

class Subject(db.Model):
    __tablename__ = "subjects"
    sub_id = db.Column(db.Integer, primary_key=True)
    sub_name = db.Column(db.Text, unique=True, nullable=False)
    
# class Notes(db.Model):
#     __tablename__ = "notes"
#     sub_id = db.Column(db.Integer, primary_key=True)
#     sub_name = db.Coumn(db.Text, unique=True, nullable=False)



# db.create_all()

def is_admin():
    users_id = [1, 2, 3]
    if current_user.id not in users_id:
        return False
    else:
        return True

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if not is_admin():
                return abort(403)
            return f(*args, **kwargs)      
        except:
              return abort(403)
    return decorated_function

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

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)
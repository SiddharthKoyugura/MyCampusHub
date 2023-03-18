from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from io import BytesIO
from PyPDF2 import PdfReader
from datetime import date

app = Flask(__name__)

app.config["SECRET_KEY"] = "ProjectBuiltByTeamTerminators"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Login Manager

login_manager = LoginManager()
login_manager.init_app(app)

# Global variables
mark_list = []
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
    attendance_percent = db.Column(db.Integer, nullable=True)

class Employee(UserMixin, db.Model):
    __tablename__ = "employees"
    eid = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=False, nullable=False)
    password = db.Column(db.Text, unique=False)
    department = db.Column(db.Text, nullable=True)
    qualification = db.Column(db.Text, nullable=True)
    gender = db.Column(db.Text, nullable=True)


class Notes(db.Model):
    __tablename__ = "notes"
    nid = db.Column(db.Integer, primary_key=True)
    sub_name = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, unique=False, nullable=False)

with app.app_context():
    db.create_all()


def is_emp():
    if current_user.eid:
        return True
    else:
        return False
    
def is_stud():
    if current_user.sid:
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

def stud_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if not is_stud():
                return abort(403)
            return f(*args, **kwargs)      
        except:
              return abort(403)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    if not is_emp():
        return Student.query.get(user_id)
    else:
        return Employee.query.get(user_id)

# Home route
@app.route("/")
def home():
    return render_template("home.html", logged_in=current_user.is_authenticated)

# Attendance section
@app.route("/attendance")
@stud_only
def attendance():
    return render_template("attendance.html", logged_in=current_user.is_authenticated)

@app.route("/add_attendance", methods=["GET", "POST"])
@emp_only
def add_attendance():
    today = date.today()
    def total_days():
        start_date = date(2023, 3, 14)
        return int((today-start_date).days)
    
    students = Student.query.all()
    if request.method=="POST":
        for student in students:
            is_present = request.form.get(str(student.sid))
            if student.attendance_percent:
                no_of_days_present = (student.attendance_percent * total_days()-1) // 100
            else:
                no_of_days_present = 0
            
            if is_present=="1":
                no_of_days_present += 1
            student.attendance_percent = int((no_of_days_present / total_days())*100)
            db.session.commit()
            mark_list.append(today)
    if date.today() in mark_list:
        is_completed = True
    else:
        is_completed = False
    return render_template("add_attendance.html", students=students, today=today, is_completed=is_completed, logged_in=current_user.is_authenticated)

# Notes routes
@app.route("/add-notes", methods=["GET", "POST"])
@emp_only
def add_notes():
    if request.method == "POST":
        new_notes = Notes(
            sub_name=request.form.get("sub_name"),
            notes=request.files["notes"].read()
        )
        db.session.add(new_notes)
        db.session.commit()
        return redirect(url_for("add_notes"))
    return render_template("add_notes.html", logged_in=current_user.is_authenticated)

@app.route("/notes")
def notes():
    notes = Notes.query.all()
    return render_template("notes.html", notes=notes, logged_in=current_user.is_authenticated)

@app.route("/download-notes/<int:nid>")
def download_notes(nid):
    notes = db.session.get(Notes, nid)
    buffer = BytesIO()
    buffer.write(notes.notes)
    pdf_reader = PdfReader(buffer)
    headers = {
        'Content-Disposition': f'attachment; filename={notes.sub_name}.pdf',
        'Content-Type': 'application/pdf'
    }
    # Return the PDF file as a Flask response
    response = make_response(pdf_reader.pages[0].extract_text())
    response.headers = headers
    return response

# Student
@app.route("/student-form", methods=["GET", "POST"])
def student_form():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        mobile = request.form.get("mobile")
        course = request.form.get("course")
        branch = request.form.get("branch")
        caste = request.form.get("caste")
        eamcet_rank = request.form.get("eamcet_rank")
        bank = request.form.get("bank")
        aadhar = request.form.get("aadhar")
        ration_card = request.form.get("ration_card")
        address = request.form.get("address")
        father_name = request.form.get("father_name")
        mother_name = request.form.get("mother_name")
        father_mobile = request.form.get("father_mobile")
        mother_mobile = request.form.get("mother_mobile")
        annual_income = request.form.get("annual_income")
        father_mail = request.form.get("father_mail")
        mother_mail = request.form.get("mother_mail")
        father_occupation = request.form.get("father_occupation")
        mother_occupation = request.form.get("mother_occupation")
        profile = request.files["image"]
        nationality = request.form.get("nationality")

        new_student = Student(
            name=name,
            email=email,
            password=password,
            mobile=mobile,
            course=course,
            branch=branch,
            caste=caste,
            eamcet_rank=eamcet_rank,
            bank=bank,
            aadhar=aadhar,
            ration_card=ration_card,
            address=address,
            father_name=father_name,
            mother_name=mother_name,
            father_mobile=father_mobile,
            mother_mobile=mother_mobile,
            annual_income=annual_income,
            father_mail=father_mail,
            mother_mail=mother_mail,
            father_occupation=father_occupation,
            mother_occupation=mother_occupation,
            profile=profile.read(),
            nationality=nationality
        )

        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for("student_form"))

    return render_template("student_form.html", logged_in=current_user.is_authenticated)

@app.route("/stu", methods=["POST"])
def stu():
    if request.method == "POST":
        email = request.form.get("email")
        user = Student.query.filter_by(email=email).first()
        if user:
            pwd = request.form.get("pwd")
            if user.password == pwd:
                login_user(user)
                return redirect(url_for("home"))
            flash("Invalid Password")
            return redirect(url_for("login"))
        flash("User not exists")
        return redirect(url_for("login"))

@app.route("/profile")
@stud_only
def profile():
    return render_template("profile.html", logged_in=current_user.is_authenticated)

# Employee
@app.route("/emp-form", methods=["GET", "POST"])
def emp_form():
    if request.method=="POST":
        new_emp = Employee(
            sub_id = request.form.get("sub_id"),
            name = request.form.get("name"),
            email = request.form.get("email"),
            password = request.form.get("password"),
            department = request.form.get("department"),
            qualification = request.form.get("qualification"),
            gender = request.form.get("gender"),
        )
        db.session.add(new_emp)
        db.session.commit()
        return redirect(url_for("emp_form"))

    return render_template("emp_form.html", logged_in=current_user.is_authenticated)

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
    return redirect(url_for("home"))
    # return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route("/logout")
@login_required
def logout():
    logout_user(current_user)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)
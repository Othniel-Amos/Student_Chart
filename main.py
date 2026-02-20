import sqlite3

from flask import Flask,render_template,flash,redirect,request,session,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functions import *
import secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(64)

def login_needed(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        if not ("user_id" in session):
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapped_function
update_subject_database() #Incase the user bothers to change the json file the code shouldn't break

@app.route("/")
def temp():
    return redirect("/index")

@app.route("/index")
@login_needed
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "user_id" in session:
            flash("Already logged in")
            return redirect("/index")
        else:
            return render_template("login.html")

    else:
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        con = get_db()
        c = con.cursor()
        c.execute('SELECT password FROM users WHERE username = ?', (username,) )


        try:
            password_database = c.fetchone()[0] #If this fails then the username must not exist
        except TypeError:
            flash("Username or password is incorrect")
            print("Empty")
            return redirect("/login")



        if check_password_hash(password_database, password): #Checks if password is correct
            con = get_db()
            c = con.cursor()
            c.execute('SELECT teacherID FROM users WHERE username = ?', (username,))
            teacher_id = int(c.fetchone()[0])


            session["user_id"] = teacher_id
            flash("Login was successful")
            return redirect("/index")
        else: # Else is not really needed but added for reading clarity
            flash("Username or password is incorrect")
            return redirect("/login")

@app.route("/homepage")
@login_needed
def homepage():
    return render_template("homepage.html")

@app.route("/add", methods=["GET","POST"])
@login_needed
def add():
    og_subjects = get_subjects() #og stands for original
    og_subjects.sort()
    grades = get_grades()
    classes = get_classes()

    if request.method == "GET":
        return render_template("add.html",subjects=og_subjects,grades=grades,classes=classes)
    else:
        fname = request.form.get("firstname").strip().title()
        lname = request.form.get("lastname").strip().title()
        grade = request.form.get("grade")
        subjects = request.form.getlist("subjects")
        myclass = request.form.get("class")
        print("\n\n\n\n\n\n\n\n\n\n") #Just to see on the cmd terminal
        print(subjects)
        valid, to_be_flashed = validate(fname,lname,grades,grade,og_subjects,subjects,classes,myclass)

        grade = int(grade)


        if valid:
            try:
                with get_db() as con:
                    c = con.cursor()
                    #See if another student exists with these exact same details
                    #Thanks to the unique constraint it shouldn't be possible to have two students with the exact same details
                    c.execute('''
                        INSERT INTO students (firstname,lastname,grade,class,teacherID) VALUES 
                        (?,?,?,?,?)''', (fname, lname, grade, myclass, session["user_id"]))
                    student_id = c.lastrowid
                    con.commit()
            except sqlite3.IntegrityError:
                flash(f"{fname} is already registered as a student")
            else: #Adds subject field
                with get_db() as con:
                    c = con.cursor()
                    placeholder = safely_add_subjects(subjects)


                    c.execute(f'''
                        SELECT subjectID FROM subjects WHERE subjectname IN ({placeholder})
                        ''',subjects)
                    subject_id_rows = c.fetchall() #ID rows of subjects in tuples


                    for subject_id in subject_id_rows:
                        subject_id = int(subject_id[0])
                        c.execute('''
                            INSERT INTO students_subjects (studentID,subjectID) 
                            VALUES (?,?)
                        ''',(student_id,subject_id))

                    con.commit()

                    flash(to_be_flashed) #Flashes that name has been added to the database
        else:
            flash(to_be_flashed) #Something in the student's field is invalid

        return redirect("/add")

@app.route("/view", methods=["GET","POST"])
@login_needed
def view(): # allows for viewing of the database
    if request.method == "GET":
        students = display_students(session["user_id"])
        print("-|" * 16)
        print(students)
        print("-|" * 16)
        return render_template("view.html",students=students)



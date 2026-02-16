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


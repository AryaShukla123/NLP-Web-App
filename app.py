from flask import Flask,render_template,request
from db import Database

app = Flask(__name__)
dbo = Database()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/perform_registration',methods=['post'])
def perform_registration():
    fname = request.form.get('user_fname')
    lname = request.form.get('user_lname')
    email = request.form.get('user_email')
    password = request.form.get('user_password')

    response = dbo.insert(fname,lname,email,password)

    if response:
        return render_template("login.html", message="Registration successful. Kindly login to proceed")
    else:
        return render_template("register.html", message="Email already exists")

    return fname + " " + lname + " " + email + " " + password

@app.route('/perform_login',methods=['post'])
def perform_login():
    email = request.form.get('user_email')
    password = request.form.get('user_password')

    response = dbo.search(email, password)

    if response:
        return "Welcome"
    else:
        return render_template("login.html", message="Incorrect email/password")



app.run(debug=True)

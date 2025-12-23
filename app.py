from flask import Flask,render_template,request,redirect
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
        return redirect('/profile')
    else:
        return render_template("login.html", message="Incorrect email/password")

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/ner')
def ner():
    return render_template('ner.html')

@app.route('/perform_ner', methods=['post'])
def perform_ner():
    text = request.form.get('ner_text')

@app.route('/sentiment')
def sentiment_analysis():
    return render_template('sentiment.html')

@app.route('/abuse')
def abuse_detection():
    return render_template('abuse.html')

@app.route('/paraphrase')
def paraphrasing():
    return render_template('paraphrase.html')

@app.route('/translate')
def translation():
    return render_template('translate.html')

@app.route('/language')
def language_detection():
    return render_template('language.html')

@app.route('/summarize')
def summarization():
    return render_template('summarize.html')

@app.route('/qa')
def question_answering():
    return render_template('qa.html')

@app.route('/semantic_search')
def semantic_search():
    return render_template('semantic_search.html')

@app.route('/semantic_similarity')
def semantic_similarity():
    return render_template('semantic_similarity.html')

@app.route('/emotion')
def emotion_detection():
    return render_template('emotion.html')



app.run(debug=True)

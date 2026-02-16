from flask import Flask,render_template,request,redirect, url_for, session
import api
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
import csv
import io
from flask import Response, make_response
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

db_url = os.getenv('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url

db = SQLAlchemy(app)

# defines User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    operation = db.Column(db.String(50), nullable=False)
    input_text = db.Column(db.Text, nullable=False)
    result = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/export_history')
def export_history():
    if 'user_email' not in session:
        return redirect('/')

    user_history = History.query.filter_by(user_email=session['user_email']).all()

    si = io.StringIO()
    cw = csv.writer(si)

    cw.writerow(['Operation', 'Input Text', 'Result'])

    for entry in user_history:
        cw.writerow([
            entry.operation,
            entry.input_text,
            entry.result
        ])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=nlp_history.csv"
    output.headers["Content-type"] = "text/csv"
    return output

with app.app_context():
    db.create_all()

# List of routes that do not require login
EXEMPT_ROUTES = ['index', 'register', 'perform_login', 'perform_registration', 'static']

@app.before_request
def check_session():

    if request.endpoint in EXEMPT_ROUTES:
        return None

    if "user_email" not in session:
        return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/perform_registration', methods=['post'])
def perform_registration():
    fname = request.form.get('user_fname')
    lname = request.form.get('user_lname')
    email = request.form.get('user_email')
    password = request.form.get('user_password')

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return render_template("register.html", message="Email already exists", category="error")

    # SQL Insert Logic
    try:

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(fname=fname, lname=lname, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return render_template("login.html", message="Registration successful. Kindly login to proceed",
                               category="success")
    except:
        db.session.rollback()
        return render_template("register.html", message="Something went wrong", category="error")


@app.route('/perform_login', methods=['post'])
def perform_login():
    email = request.form.get('user_email')
    password = request.form.get('user_password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session["user_email"] = user.email
        session["user_name"] = f"{user.fname} {user.lname}"
        return redirect('/profile')
    else:
        return render_template("login.html", message="Incorrect email/password", category="error")

@app.route('/view_history')
def view_history():
    # Find all history records for the logged in user
    user_history = History.query.filter_by(user_email=session['user_email']).all()
    return render_template('history.html', history=user_history)


@app.route('/delete_history/<int:id>')
def delete_history(id):
    item = History.query.get(id)

    # Security check
    if item and item.user_email == session['user_email']:
        db.session.delete(item)
        db.session.commit()

    return redirect('/view_history')


@app.route('/clear_all_history')
def clear_all_history():
    # Delete all records for the current user
    History.query.filter_by(user_email=session['user_email']).delete()
    db.session.commit()
    return redirect('/view_history')

@app.route('/profile')
def profile():
    if 'user_email' not in session:
        return redirect('/')

    # Generate Avatar URL using the user's email
    email = session['user_email']
    avatar_url = f"https://api.dicebear.com/7.x/bottts/svg?seed={email}"

    # Query to count occurrences of each operation for the logged-in user
    stats_query = db.session.query(
        History.operation,
        func.count(History.id)
    ).filter_by(user_email=session['user_email']).group_by(History.operation).all()

    # Convert to format Chart.js likes
    labels = [row[0] for row in stats_query]
    values = [row[1] for row in stats_query]

    return render_template('profile.html', labels=labels, values=values, avatar_url=avatar_url)

@app.route('/ner')
def ner():

    return render_template('ner.html')

@app.route('/sentiment')
def sentiment_analysis():

    return render_template('sentiment.html')

@app.route("/perform_sentiment", methods=["POST"])
def perform_sentiment():
    text = request.form.get("text")

    if not text:
        return render_template("sentiment.html", result="Please enter some text")

    result = api.sentiment_analysis(text)

    new_history = History(
        user_email=session['user_email'],
        operation="Sentiment Analysis",
        input_text=text,
        result=str(result)
    )
    db.session.add(new_history)
    db.session.commit()

    print("🔥 SENTIMENT RESULT:", result)
    return render_template("sentiment.html", result=result)


@app.route('/abuse')
def abuse_detection():

    return render_template('abuse.html')

@app.route("/perform_abuse", methods=["GET", "POST"])
def perform_abuse():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        result = api.abuse_detection(text)

        new_history = History(
            user_email=session['user_email'],
            operation="Abuse Detection",
            input_text=text,
            result=str(result)
        )
        db.session.add(new_history)
        db.session.commit()

    return render_template("abuse.html", result=result)

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

@app.route("/perform_ner", methods=["GET","POST"])
def perform_ner():
    text = request.form["text"]
    entities = api.ner(text)

    new_history = History(
        user_email=session['user_email'],
        operation="Named Entity Recognition",
        input_text=text,
        result=str(entities)
    )
    db.session.add(new_history)
    db.session.commit()

    return render_template("ner.html", entities=entities)


@app.route("/perform_paraphrase", methods=["GET", "POST"])
def perform_paraphrasing():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        result = api.paraphrase(text)

        new_history = History(
            user_email=session['user_email'],
            operation="Paraphrasing",
            input_text=text,
            result=str(result)
        )
        db.session.add(new_history)
        db.session.commit()

    return render_template("paraphrase.html", result=result)


@app.route("/perform_translate", methods=["POST"])
def perform_translation():
    text = request.form["text"]
    source_lang = request.form["source_lang"]
    target_lang = request.form["target_lang"]

    result = api.translate_text(text, source_lang, target_lang)

    new_history = History(
        user_email=session['user_email'],
        operation=f"Translation ({source_lang} to {target_lang})",
        input_text=text,
        result=str(result)
    )
    db.session.add(new_history)
    db.session.commit()

    return render_template("translate.html", result=result)


@app.route("/perform_language", methods=["GET", "POST"])
def perform_language():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        result = api.language_detection(text)

        new_history = History(
            user_email=session['user_email'],
            operation="Language Detection",
            input_text=text,
            result=str(result)
        )
        db.session.add(new_history)
        db.session.commit()

    return render_template("language.html", result=result)


@app.route("/perform_summary", methods=["GET", "POST"])
def perform_summary():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        result = api.summarization(text)

        new_history = History(
            user_email=session['user_email'],
            operation="Summarization",
            input_text=text,
            result=str(result)
        )
        db.session.add(new_history)
        db.session.commit()

    return render_template("summarize.html", result=result)


@app.route("/perform_qa", methods=["GET", "POST"])
def perform_qa():
    result = ""
    if request.method == "POST":
        context = request.form["context"]
        question = request.form["question"]
        result = api.question_answering(context, question)

        new_history = History(
            user_email=session['user_email'],
            operation="Question Answering",
            input_text=f"Q: {question} | Context: {context[:50]}...",
            result=str(result)
        )
        db.session.add(new_history)
        db.session.commit()

    return render_template("qa.html", result=result)


@app.route("/perform_semantic-search", methods=["POST"])
def perform_semantic_search():
    result = ""
    if request.method == "POST":
        query = request.form["query"]
        documents = request.form["documents"]
        result = api.semantic_search(query, documents)

        new_history = History(
            user_email=session['user_email'],
            operation="Semantic Search",
            input_text=f"Query: {query}",
            result=str(result)
        )
        db.session.add(new_history)
        db.session.commit()

    return render_template("semantic_search.html", result=result)

@app.route("/perform_semantic-similarity", methods=["GET", "POST"])
def perform_semantic_similarity():
    result = ""
    if request.method == "POST":
        text1 = request.form["text1"]
        text2 = request.form["text2"]
        data = api.semantic_similarity(text1, text2)

        new_history = History(
            user_email=session['user_email'],
            operation="Semantic Similarity",
            input_text=f"T1: {text1[:30]}.. | T2: {text2[:30]}..",
            result=f"Score: {data['score']} | {data['explanation']}"
        )
        db.session.add(new_history)
        db.session.commit()

        return render_template(
            "semantic_similarity.html",
            score=data["score"],
            result=data["explanation"]
        )

@app.route("/perform_emotion", methods=["GET", "POST"])
def perform_emotion():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        result = api.emotion_detection(text)

        new_history = History(
            user_email=session['user_email'],
            operation="Emotion Detection",
            input_text=text,
            result=str(result)
        )
        db.session.add(new_history)
        db.session.commit()

    return render_template("emotion.html", result=result)


@app.route('/settings')
def settings():
    if 'user_email' not in session:
        return redirect('/')
    user = User.query.filter_by(email=session['user_email']).first()
    return render_template('settings.html', user=user)


@app.route('/update_profile', methods=['POST'])
def update_profile():
    user = User.query.filter_by(email=session['user_email']).first()
    user.fname = request.form.get('fname')
    user.lname = request.form.get('lname')

    # Update session name too
    session['user_name'] = f"{user.fname} {user.lname}"

    db.session.commit()
    return redirect('/profile')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask,render_template,request,redirect
from db import Database
import api

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

@app.route('/sentiment')
def sentiment_analysis():
    return render_template('sentiment.html')

@app.route("/perform_sentiment", methods=["POST"])
def perform_sentiment():
    text = request.form.get("text")

    if not text:
        return render_template("sentiment.html", result="Please enter some text")

    result = api.sentiment_analysis(text)

    print("🔥 SENTIMENT RESULT:", result)  # DEBUG LINE

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
    return render_template("ner.html", entities=entities)



@app.route("/perform_paraphrase", methods=["GET", "POST"])
def perform_paraphrasing():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        result = api.paraphrase(text)
    return render_template("paraphrase.html", result=result)


@app.route("/perform_translate", methods=["POST"])
def perform_translation():
    text = request.form["text"]
    source_lang = request.form["source_lang"]
    target_lang = request.form["target_lang"]

    result = api.translate_text(text, source_lang, target_lang)

    return render_template(
        "translate.html",
        result=result
    )



@app.route("/perform_language", methods=["GET", "POST"])
def perform_language():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        result = api.language_detection(text)
    return render_template("language.html", result=result)


@app.route("/perform_summary", methods=["GET", "POST"])
def perform_summary():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        result = api.summarize(text)
    return render_template("summary.html", result=result)


@app.route("/perform_qa", methods=["GET", "POST"])
def perform_qa():
    result = ""
    if request.method == "POST":
        context = request.form["context"]
        question = request.form["question"]
        result = api.question_answer(context, question)
    return render_template("qa.html", result=result)


@app.route("/perform_semantic-search", methods=["GET", "POST"])
def perform_semantic_search():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        result = api.semantic_search(text)
    return render_template("semantic_search.html", result=result)


@app.route("/perform_semantic-similarity", methods=["GET", "POST"])
def perform_semantic_similarity():
    result = ""
    if request.method == "POST":
        text1 = request.form["text1"]
        text2 = request.form["text2"]
        result = api.semantic_similarity(text1, text2)
    return render_template("semantic_similarity.html", result=result)


@app.route("/perform_emotion", methods=["GET", "POST"])
def perform_emotion():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        result = api.emotion_detection(text)
    return render_template("emotion.html", result=result)



app.run(debug=True)

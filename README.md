# NLP Web Assistant 🚀

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://ai.google.dev/)
[![Render](https://img.shields.io/badge/Render-%2346E3B7.svg?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)

A professional Flask-based web application that leverages Google's **Gemini 1.5 Flash** model to provide powerful Natural Language Processing (NLP) tools. This application features a secure user authentication system and a suite of AI-driven text analysis capabilities.

---

## 🔗 Live Demo
**Check out the live application here:**
### [👉 NLP Web Assistant on Render](https://nlp-web-app-ri3r.onrender.com) 
*(Note: Please allow 1 minute for the server to "wake up" on the first visit)*

---

## Features

### 1. User Authentication System
* **Secure Registration & Login**: Users can create private accounts to access personalized NLP tools.
* **Session Management**: Powered by Flask-Session to ensure a seamless and secure user experience.
* **Status Feedback**: Real-time color-coded alerts for login errors and successful registrations.

### 2. AI-Powered NLP Tools
* **Sentiment Analysis**: Accurately detects the emotional tone (Positive, Negative, Neutral) of any text.
* **Entity Extraction**: Automatically identifies and categorizes key names, places, and organizations.
* **Text Summarization**: Uses Gemini's reasoning to condense long articles into short, readable summaries.
* **Language Translation**: High-fidelity translation across multiple global languages.

### 3. Modern User Interface
* **Responsive Design**: Optimized for both desktop and mobile viewing.
* **Clean Layout**: A distraction-free environment designed for productivity.

---

## Tech Stack

* **Backend:** Python 3.x, Flask
* **AI Engine:** Google GenAI (Gemini 1.5 Flash)
* **Database:** JSON-based persistent storage (expandable to PostgreSQL)
* **Frontend:** HTML5, CSS3, Jinja2 Templates
* **Deployment:** Render (WSGI with Gunicorn)

---

## Installation & Setup

To run this project locally, follow these steps:

### 1. Clone the repository
```bash
git clone [https://github.com/AryaShukla123/NLP-Web-App.git](https://github.com/AryaShukla123/NLP-Web-App.git)
cd NLP-Web-App
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a ```.env``` file in the root directory:
```bash
SECRET_KEY=your_flask_secret_key
MY_NLP_API_KEY=your_google_gemini_api_key
```

### 5. Run the Application
```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.


---


## 📩 Contact & Connect

If you have any questions or would like to discuss this project, feel free to reach out!

* **Name:** Arya Shukla
* **GitHub:** [@AryaShukla123](https://github.com/AryaShukla123)
* **LinkedIn:** [Arya Shukla](www.linkedin.com/in/arya-shukla-3517a3322)
* **Email:** [arya.bnsd@gmail.com](mailto:arya.bnsd@gmail.com)

---
**Made with ❤️ and Python**
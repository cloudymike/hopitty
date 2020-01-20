import json
from app import app
from app import google_auth
from flask import render_template

@app.route('/hello')
def hello():
    return "Hello, World!"

@app.route('/')
@app.route('/index')
def index():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
    else:
        user_info = None

    return render_template('index.html', title='Home', user=user_info)

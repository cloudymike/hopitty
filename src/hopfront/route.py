
import hopfront
from hopfront import mqttsock
from flask import Flask, render_template, flash, redirect, url_for
from hopfront import CmdForm, LoadForm
import sys
import json
import time
import argparse

from hopfront import google_auth

from hf import app



@app.route('/')
@app.route('/index')
def index():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
    else:
        user_info = None

    return render_template('index.html', title='Home', user=user_info)
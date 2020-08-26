# app.py

from flask import Flask, render_template, flash, redirect, url_for
from flask import jsonify
from forms import CmdForm, LoadForm, RecipeForm
import requests
import boto3
import os

import google_auth
import command
import brewstatus



# Initialize dynamodb access
dynamodb = boto3.resource('dynamodb')
db = dynamodb.Table('zappatutorial')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cEumZnHA5QvxVDNXfazEDs7e6Eg368yD'
app.register_blueprint(google_auth.app)

@app.route('/')
@app.route('/index')
def index():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
    else:
        user_info = None
    return render_template('index.html', title='Home', user=user_info)

@app.route('/cmd', methods=['GET', 'POST'])
def cmd():
    if not google_auth.is_logged_in():
        return (redirect('/'))
    # TODO read the state
    current_state = 'stop'
    form = CmdForm(command=current_state)

    if form.validate_on_submit():
        print('Got command {}'.format(form.command.data))
        if form.command.data in ['terminate','pause','run', 'stop', 'skip']:
            try:
                command.command(form.command.data)
            except:
                print('Can not communicate with controller')
    return render_template('cmd.html', title='Command', form=form)

@app.route('/status')
def status():
    response=brewstatus.fullstatus()
    return render_template('generic.html', title='Terminate', response=response)

















@app.route('/counter', methods=['GET'])
def counter_get():
    res = db.get_item(Key={'id': 'counter'})
    testval = res['Item']['testval']
    counter_value = str(res['Item']['counter_value'])
    jsonval = jsonify({'testval': testval, 'counter_value': counter_value})
    return(jsonval)

@app.route('/counter/increase', methods=['POST'])
def counter_increase():
    res = db.get_item(Key={'id': 'counter'})
    value = res['Item']['counter_value'] + 1
    res = db.update_item(
        Key={'id': 'counter'},
        UpdateExpression='set counter_value=:value',
        ExpressionAttributeValues={':value': value},
        )
    strvalue = str(value)
    return jsonify({'counter': strvalue})

# We only need this for local development.
if __name__ == '__main__':


    app.run()

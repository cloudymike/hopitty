from flask import Flask, render_template, flash, redirect, url_for
from forms import CmdForm, LoadForm, RecipeForm
import sys
import json
import time
import argparse
import requests


import google_auth
import recipelist

import brewque


RECIPE_CHOICES=[('porter','porter'),('saison','saison'),('IPA','IPA'),('NEIPA','NEIPA'),('wit','wit')]



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
    current_state = bq.get_state()
    form = CmdForm(command=current_state)

    if form.validate_on_submit():
        print('Got command {}'.format(form.command.data))
        if form.command.data in ['terminate','pause','run', 'stop', 'skip']:
            try:
                data = bq.put_command(form.command.data)
            except:
                print('Can not communicate with controller')
        #return redirect(url_for('index'))
    print('rerendering')
    #time.sleep(4)
    return render_template('cmd.html', title='Command', form=form)

@app.route('/status')    
def status():
    if not google_auth.is_logged_in():
        return (redirect('/'))
    current_status = bq.get_status()
    return render_template('status.html', title='Status', current_status = current_status)


@app.route('/list', methods=['GET', 'POST'])
def list():
    if not google_auth.is_logged_in():
        return (redirect('/'))
    recipeNameList = dynamorl.get_recipeNameList()
    recipeNameStr = ''
    for recipeName in recipeNameList:
        recipeNameStr = recipeNameStr + '<p>' +recipeName + '</P>\n'
    return(recipeNameStr)
 
    current_recipe = 'porter'
    
    form = RecipeForm(recipe=current_recipe)

    if form.validate_on_submit():
        print('Got Recipe {}'.format(form.recipe.data))
        try:
            print('Load recipe here')
            #data = comm_client.write_command(form.command.data)
        except:
            print('Can not communicate with controller')
        #return redirect(url_for('index'))
    print('rerendering')
    #time.sleep(4)
    return render_template('recipe.html', title='Recipe', form=form)
   

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--mqtt", action='store_true', help='Use mqtt communication')
    group.add_argument("-a", "--aws", action='store_true', help='Use aws mqtt communication')
    args = parser.parse_args()
    
    if args.mqtt:
        bq = brewque.brewque(connection='localhost')
    if args.aws:
         bq = brewque.brewque(connection='aws')
        
    dynamorl = recipelist.recipelist()    
    
    # Wait for a message to appear
    time.sleep(2)


    app.run(host='0.0.0.0', port=8080)

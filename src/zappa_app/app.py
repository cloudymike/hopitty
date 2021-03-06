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
import dynamorecipelist


dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
statusdb = brewstatus.dynamostatus(dynamodb)
dynamorl = dynamorecipelist.dynamorecipelist(dynamodb=dynamodb)

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
    current_state = statusdb.get_state()
    form = CmdForm(command=current_state)

    if form.validate_on_submit():
        print('Got command {}'.format(form.command.data))
        if form.command.data in ['terminate','pause','run', 'stop', 'skip']:
            try:
                command.command(form.command.data)
            except:
                print('Can not communicate with controller')
    return render_template('cmd.html', title='Command', form=form)


@app.route('/list', methods=['GET', 'POST'])
def list():
    if not google_auth.is_logged_in():
        return (redirect('/'))
    equipmentname = statusdb.get_equipmentname()
    if not equipmentname:
        return(render_template('generic.html',title='Recipe', response='No controller or recipes available'))
    dynamorl.set_equipmentname(equipmentname)
    recipeNameList = dynamorl.get_recipeNameList()
    recipeTupleList = []
    for recipename in recipeNameList:
        recipeTuple = (recipename, recipename)
        recipeTupleList.append(recipeTuple)

    # This should come from brewstatus
    current_recipe = statusdb.get_recipename()
    form = RecipeForm(recipe=current_recipe)
    form.recipe.choices = recipeTupleList

    if form.validate_on_submit():
        recipe2load = dynamorl.get_loadable_recipe(form.recipe.data, equipmentname)
        try:
            print('Loading recipe {}'.format(form.recipe.data))
            command.put_recipe(recipe2load)
        except:
            print('Can not communicate with controller')
    print('rerendering')
    return render_template('recipe.html', title='Recipe', form=form)


@app.route('/status')
def status():
    if not google_auth.is_logged_in():
        return (redirect('/'))
    current_status = statusdb.get_controller_status()
    if current_status:
        stage = statusdb.get_stage()
        return render_template('status.html', title='Status', current_status=current_status, stage=stage)
    else:
        return(render_template('generic.html',title='Status', response='No brew controller available'))

















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

from flask import Flask, render_template, flash, redirect, url_for, make_response
from forms import CmdForm, LoadForm, RecipeForm
import sys
import json
import time
import argparse
import requests

import boto3


#import google_auth
import dynamorecipelist
import brewque


RECIPE_CHOICES=[('porter','porter'),('saison','saison'),('IPA','IPA'),('NEIPA','NEIPA'),('wit','wit')]

hostname = '192.168.62.151'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cEumZnHA5QvxVDNXfazEDs7e6Eg368yD'
#app.register_blueprint(google_auth.app)

@app.route('/')
@app.route('/index')
def index():
#    if google_auth.is_logged_in():
#        user_info = google_auth.get_user_info()
#    else:
    user_info = None
    return render_template('index.html', title='Home', user=user_info)

@app.route('/cmd', methods=['GET', 'POST'])
def cmd():
#   if not google_auth.is_logged_in():
#        return (redirect('/'))
    current_state = bq.get_state()
    form = CmdForm(command=current_state)

    if form.validate_on_submit():
        print('Got command {}'.format(form.command.data))
        if form.command.data in ['terminate','pause','run', 'stop', 'skip']:
            try:
                data = bq.put_command(form.command.data)
            except:
                print('Can not communicate with controller')
    return render_template('cmd.html', title='Command', form=form)

@app.route('/status')
def status():
#    if not google_auth.is_logged_in():
#        return (redirect('/'))
    current_status = bq.get_controller_status()
    return render_template('status.html', title='Status', current_status = current_status)

@app.route('/metricsox')
def metricsox():
#    if not google_auth.is_logged_in():
#        return (redirect('/'))
    current_status = bq.get_controller_status()
    return('# HELP bogus bogus variable # TYPE bogus bogus 1.0')
    #return render_template('metrics.html', title='metrics', current_status = current_status)

def generateMetrics():
    current_status = bq.get_controller_status()
    #current_status = [["tmp1", 100],["vol2",3]]
    status_string = ""
    for status in current_status:
        status_string = "{} # TYPE {} gauge\n{} {}\n".format(status_string,status[0], status[0], status[1])
    return(status_string)


@app.route('/metrics')
def metrics():
    response = make_response(generateMetrics(), 200)
    response.mimetype = "text/plain"
    return response


@app.route('/graph')
def graph():
    prom_url = "http://{}:3000/d/HOPITTYVAR/hopittyvar?orgId=1&refresh=1m".format(hostname)
    print(prom_url)

    return render_template('graph.html', 
        title='Graph',
        frame_url=prom_url,
    )



@app.route('/list', methods=['GET', 'POST'])
def list():
#    if not google_auth.is_logged_in():
#        return (redirect('/'))
    equipmentname = bq.get_equipmentname()
    dynamorl.set_equipmentname(equipmentname)
    recipeNameList = dynamorl.get_recipeNameList()
    recipeTupleList = []
    for recipename in recipeNameList:
        recipeTuple = (recipename, recipename)
        recipeTupleList.append(recipeTuple)

    # This should come from brewque
    current_recipe = bq.get_recipename()
    form = RecipeForm(recipe=current_recipe)
    form.recipe.choices = recipeTupleList

    if form.validate_on_submit():
        print('Got Recipe {}'.format(form.recipe.data))
        recipe2load = dynamorl.get_loadable_recipe(form.recipe.data, equipmentname)
        print('Recipe to load: {}'.format(recipe2load))
        try:
            print('Load recipe here')
            bq.put_recipe(recipe2load)
        except:
            print('Can not communicate with controller')
        #return redirect(url_for('index'))
    print('rerendering')
    #time.sleep(4)
    return render_template('recipe.html', title='Recipe', form=form)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', '--Dynamodb', default=None, type=str, help='URL for dynamoDB ')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--mqtt", action='store_true', help='Use mqtt communication')
    group.add_argument("-a", "--aws", action='store_true', help='Use aws mqtt communication')
    group.add_argument("-H", "--HOST", default=None, type=str, help='Use HOST as mqtt server')

    args = parser.parse_args()

    if args.mqtt:
        bq = brewque.brewque(connection='localhost')
    if args.aws:
        bq = brewque.brewque(connection='aws')
    if args.HOST:
        bq = brewque.brewque(connection=args.HOST)


    # Wait for a message to appear
    time.sleep(2)
    if args.Dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=args.Dynamodb, region_name='us-east-2')
        print("Dynamodb on {}".format(args.Dynamodb))
    else:
        dynamodb = None
    dynamorl = dynamorecipelist.dynamorecipelist(bq.get_equipmentname(),dynamodb)

    app.run(host='0.0.0.0', port=8080)



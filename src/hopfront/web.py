import netsock
import mqttsock
from flask import Flask, render_template, flash, redirect, url_for
from forms import CmdForm, LoadForm
import sys
import json
import time
import argparse

import google_auth
import route


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cEumZnHA5QvxVDNXfazEDs7e6Eg368yD'
app.register_blueprint(google_auth.app)
app.register_blueprint(route.app)

#import recipeModel
def readRecipeFile(recipefile=None, user='mikael'):
    rl = recipeModel.RecipeList()

    # Try to find a recipe file
    if recipefile is not None:
        bsmxfile = recipefile
    elif user is not None:
        bsmxfile = "/home/" + user + "/.beersmith2/Cloud.bsmx"
    else:
        print("ERROR: No data for BSMX file")
        bsmxfile = None

    print(bsmxfile)

    if path.isfile(bsmxfile) and access(bsmxfile, R_OK):
        print("BSMX File", bsmxfile, "exists and is readable")
    else:
        print("ERROR: BSMX file", bsmxfile,\
              "is missing or is not readable")
        bsmxfile = None

    rl.readBeerSmith(bsmxfile)

    print("================ Recipe List ===============")
    rl.printNameList()
    print("============================================")
    return(rl)






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

    try:
        current_status = comm_client.read_status()
        status_string = str(current_status).replace("'","")
        statusdict = json.loads(status_string)
        current_state = statusdict['state']
    except:
        print('Can not communicate with controller')
        current_status = 'Controller failing'
        current_state = "stop"

    form = CmdForm(command=current_state)

    if form.validate_on_submit():
        print('Got command {}'.format(form.command.data))
        if form.command.data in ['terminate','pause','run', 'stop', 'skip']:
            try:
                data = comm_client.write_command(form.command.data)
            except:
                print('Can not communicate with controller')
        #return redirect(url_for('index'))
    print('rerendering')
    #time.sleep(4)
    return render_template('cmd.html', title='Command', form=form)

@app.route('/list')
def list():
    if not google_auth.is_logged_in():
        return (redirect('/'))
    try:
        recipelist = readRecipeFile()
    except:
        print('Can not find recipes')
        current_status = 'No recipes'
    return render_template('status.html', title='Recipes', current_status = recipelist)


@app.route('/load', methods=['GET', 'POST'])
def load():
    if not google_auth.is_logged_in():
        return (redirect('/'))

    form = LoadForm()
    
    if form.validate_on_submit():
        try:
            data = comm_client.write(form.load.data)
        except:
            print('Can not communicate with controller')
        print("Stages: {}".format(form.load.data))
        print('back to index, just kiddin')
        return redirect(url_for('index'))
        
    stages_example={}
    stages_example['s1'] = {}
    stages_example['s1']['cycles'] = 3
    stages_example['s2'] = {}
    stages_example['s2']['cycles'] = 4
    stages_string = json.dumps(stages_example)

    return render_template('load.html', title='Load', form=form, stages_example=stages_string)



if __name__ == "__main__":
    global comm_client
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--netsock", action='store_true', help='Use netsock communication')
    group.add_argument("-m", "--mqtt", action='store_true', help='Use mqtt communication')
    group.add_argument("-a", "--aws", action='store_true', help='Use aws mqtt communication')
    args = parser.parse_args()
    
    if args.netsock:
        comm_client = netsock.socketclient()
    if args.mqtt:
        comm_client = mqttsock.socketclient(connection='localhost')
    if args.aws:
        comm_client = mqttsock.socketclient(connection='aws')
        
    # Wait for a message to appear
    time.sleep(2)


    app.run(host='0.0.0.0', port=8080)

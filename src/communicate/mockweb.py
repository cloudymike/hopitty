import netsock
from flask import Flask, render_template, flash, redirect, url_for
from forms import CmdForm, LoadForm
import sys
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cEumZnHA5QvxVDNXfazEDs7e6Eg368yD'

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Brewer'}
    return render_template('index.html', title='Home', user=user)
    
@app.route('/cmd', methods=['GET', 'POST'])
def cmd():

    form = CmdForm()
    
    if form.validate_on_submit():
        print('Got command {}'.format(form.command.data))
        if form.command.data in ['terminate','pause','run', 'stop', 'skip']:
            try:
                data = netsock.write(form.command.data)
            except:
                print('Can not communicate with controller')
        print('back to index, just kiddin')
        return redirect(url_for('index'))
    print('rerendering')
    return render_template('cmd.html', title='Command', form=form)

@app.route('/status')    
def status():
    try:
        current_status = netsock.write('status')
    except:
        print('Can not communicate with controller')
        current_status = 'Controller failing'
    return render_template('status.html', title='Status', current_status = current_status) 


@app.route('/load', methods=['GET', 'POST'])
def load():

    form = LoadForm()
    
    if form.validate_on_submit():
        try:
            data = netsock.write(form.load.data)
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
    app.run(host='0.0.0.0', port=8080)

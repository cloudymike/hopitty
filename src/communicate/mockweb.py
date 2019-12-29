import netsock
from flask import Flask 
from flask import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cEumZnHA5QvxVDNXfazEDs7e6Eg368yD'

@app.route("/")
@app.route('/index')
def hello():
    user = {'username': 'Mikael'}
    return render_template('index.html', title='Home', user=user)
    
@app.route("/terminate")
def terminate():
    data = netsock.write('terminate')
    return "Terminating..."



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

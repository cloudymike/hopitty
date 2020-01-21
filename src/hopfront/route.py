from flask import render_template, redirect, url_for, Blueprint

import google_auth

#from web import comm_client

app = Blueprint('route', __name__)


@app.route('/status')
def status():
    if not google_auth.is_logged_in():
        return (redirect('/'))
    try:
        current_status = comm_client.read_status()
        print(current_status)
    except:
        print('Can not communicate with controller')
        current_status = 'Controller failing'
    return render_template('status.html', title='Status', current_status = current_status)



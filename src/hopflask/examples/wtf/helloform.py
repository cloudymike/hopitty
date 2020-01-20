from flask import Flask, redirect, render_template
from myform import MyForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cEumZnHA5QvxVDNXfazEDs7e6Eg368yD'

@app.route("/", methods=('GET', 'POST'))
def hello():
    return "Hello World!"

@app.route("/success", methods=('GET', 'POST'))
def success():
    return "Success!"

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    print form.name.data
    if form.validate_on_submit():
        print form.name.data
        return redirect('/success')
    print('Going nowhere')
    return render_template('submit.html', form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

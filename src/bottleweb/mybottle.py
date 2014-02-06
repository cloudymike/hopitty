from bottle import route, run, template, error, get, post
from bottle import request, response, redirect
import bottle
import time

counter = 1


def update_counter():
    global counter
    counter = counter + 1


@route('/')
@route('/hello/<name>')
def index(name='world'):

    if request.get_cookie("hello_visited"):
        return template("Welcome back {{name}}</b>! Nice to see you again",\
                name=name)
    else:
        response.set_cookie("hello_visited", "yes", max_age=60)
        return template('<b>Hello {{name}}</b>! Nice to meet you', name=name)


@route('/pretty')
def pretty():
    dapage = '''
    <h1>Big head</h1>
    hi
    '''
    return(dapage)


@route('/refresh')
def pretty():
#    dapage=template('<b>Count is {{counter}}</b>', counter=counter)
    dapage = """
    <meta http-equiv="refresh" content="5">
    %i
    """ % counter
    update_counter()
#    time.sleep(1)
    return(dapage)


@get('/me')
def me():
    return '''
        <form action="/me" method="post">
            Username: <input name="username" type="text" />
            <input value="Login" type="submit" />
        </form>
    '''


@post('/me')  # or @route('/login', method='POST')
def do_me_in():
    username = request.forms.get('username')
    if username == 'mikael':
        return "<p>Your username is correct.</p>"
    else:
        return "<p>That's not a good one.</p>"


@error(404)
def error404(error):
    return 'These are not the droids you are looking for'


@route('/wrong')
def wrong():
    redirect("/")


bottle.debug(True)
run(host='0.0.0.0', port=8080)

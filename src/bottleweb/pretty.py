from bottle import route, run, template, error, get, post
from bottle import request, response, redirect
import bottle


@route('/pretty')
def pretty():
    dapage = '''
    <h1>Big head</h1>
    hi
    '''
    return(dapage)

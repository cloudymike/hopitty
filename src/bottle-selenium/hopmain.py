from bottle import run, route, request, template
import sys
sys.path.append("../")
from bottleweb import index


if __name__ == '__main__':
    run(reloader=True)

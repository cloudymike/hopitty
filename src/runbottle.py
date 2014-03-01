#!/usr/bin/python

import bottleweb
from bottle import run


def begin():
    run(server=server)


if __name__ == '__main__':
    server = bottleweb.mybottle(host="0.0.0.0", port=8080)
    server.quiet = False
    begin()

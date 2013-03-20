#!/usr/bin/python

"""
Test page of classes used in web pages
"""

import commonweb
import dataMemcache


if __name__ == "__main__":
    cw = commonweb.commonweb()
    cw.header("hello page")
    hi = dataMemcache.helloData()
    print hi.getData()
    cw.footer(__file__)

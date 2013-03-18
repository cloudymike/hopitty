hopitty
=======

Python controller

How to run
==========
cd src

For one recipe run:
./runctrl.py -f ../recipes/something

Reading all beersmith recipes:
./runscan.py

Web pages
=========
(This may change)
The web pages are independent of the controller and communicates
with memcache

The scripts are mainly status script with addition of, when using runscan.py,
allowing for selection of recipe and start a run

To install cgi-bin scripts, cd into src/cgibin and type sudo INSTALL

Note cgi-bin is not a valid python module name so the dir needs to be cgibin.
Otherwise many things will break including nosetests.

How to build
============
SETUP

Should do something like this:
# Python packages. May require github downloads
easy_install python-x10
easy_install pyusb
easy_install pyserial
cd GoIO-2.28.0
# May need to run ./configure
./INSTALL
cd mytemp
make


Notes on pumps
===============
Four gallon => 3.5 gallons

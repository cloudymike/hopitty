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

Got to web page:
http://localhost

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
The script SETUP in top dir should install all dependencies and run the tests.
If errors, check the script. It relies on the ability to download from different
vendors.

This script will also setup the required web pages into /var/www

Testing
=======
The script checkall should do a comprehensive test. It will run a number of
nose tests and then also a set of functional tests as well as a lint. IF any fails
it will stop the tests.

Hardware specific code
=======================
There are some code that is not python, that is required to control the hardware.
The code is all compiled within the setup script to allow portability. For details
check the web pages of the vendors. The wget statement in SETUP is a good hint.

Customization
=============
To change this program for different equipment there are two files that needs to be modified.

ctrl/rununit.py:
In function setupControllers, define the controllers(appliances) to be used. In most cases,
you can leave controllers in, that are not called by recipe, without harm.

In additon if you have specific hardware (USB devices) you may need to add 
these in switches, sensors and appliances. There are generic examples of all
of this to start from, and should be inherited.

If you like to create your own cont

ctrl/mashProfiles.py: 
This file include the translation from the BeerSmith recipe to 
a stages dictionary, defining how the controller is to be run.



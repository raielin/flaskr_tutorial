# FILE: flaskr/flaskr.py
# REFERENCE: http://flask.pocoo.org/docs/0.10/tutorial/setup/#tutorial-setup
# CMD: start up application with: `$ python flaskr.py`


# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

# configuration
# per tutorial: ok in small apps to drop config directly into module.
# cleaner solution would be to create separate `.ini` or `.py` file and load that or import the values from there.
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create flaskr application and initialize it with the config from the same file, in flaskr.py
app = Flask(__name__)
app.config.from_object(__name__)

# method to connect to specified database. can be used to open a connection on request and also from Python shell or a script.
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# check to fire up server if we want to run this file as a standalone application
if __name__ == '__main__':
    app.run()


# -------------------------------------
# NOTES:
# -------------------------------------

# from_object() looks at given object (will import it if it's a string) and then look for all uppercase variables defined there. in this case, the 'configuration' section directly above, but could also be from a separate file.

# alternative to from_object() is from_envvar(). allows you to load a configuration from a configurable file.
    # app.config.from_envvar('FLASKR_SETTINGS', silent=True)
       # a user can sent an environment variable called FLASKR_SETTINGS to specifiy a config file to be loaded which will override the default values. the silent switch tells Flask not to complain if no such environment key is set.





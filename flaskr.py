# FILE: flaskr/flaskr.py
# REFERENCE: http://flask.pocoo.org/docs/0.10/tutorial/setup/#tutorial-setup
# CMD: start up application with: `$ python flaskr.py`


# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing

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

# create function to initialize the database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
# Create database in Python shell:
    # >>> from flaskr import init_db
    # >>> init_db()

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

# closing() helper function used in database initialization allows connection to stay open for duration of the `with` block.

# app.open_resource() supports ability to operate for duration of the `with` block inherently, so can be used in `with` block directly.
    # opens file from the resource location (in this case, our flaskr directory) and allows the program to read from it. in this case, we are using it to execute a script on the database connection which is saved in `schema.sql`.

# db.commit() to commit changes. SQLite 3 and other transactional databases will not commit unless you explicityly tell it to.

# If you get an exception later that a table cannot be found check that you did call the init_db function and that your table names are correct (singular vs. plural for example).

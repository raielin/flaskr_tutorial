# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~
    A microblog example application written as Flask tutorial with
    Flask and sqlite3.
    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

# FILE: flaskr/flaskr.py
# REFERENCE: http://flask.pocoo.org/docs/0.10/tutorial/setup/#tutorial-setup
# CMD: start up application with: `$ python flaskr.py`


# all the imports
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# create flaskr application and initialize it with the config from the same file, in flaskr.py
app = Flask(__name__)

# configuration
# load default config and override config from an environment variable
    # per tutorial: ok in small apps to drop config directly into module.
    # cleaner solution would be to create separate `.ini` or `.py` file and load that or import the values from there.
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# method to connect to specified database. can be used to open a connection on request and also from Python shell or a script.
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.row
    return rv

# create function to initialize the database
def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
# Create database in Python shell:
    # >>> from flaskr import init_db
    # >>> init_db()

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

# Initialize DB connections before each request & shut them down afterwards.
# before_request() is called before a request and passed no arguments.
# @app.before_request
# def before_request():
#     g.db = connect_db()

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# teardown_appcontext() gets called after the response has been constructed.
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
      g.sqlite_db.close()

# show_entries() view function passes entries as dicts to the show_entries.html template and returns the rendered one.
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

# add_entry() view function lets user add new entries with a form on the show_entries page if they are logged in. function only responds to POST requests.
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    # use question marks when building SQL statements, otherwise will be vulnerable to SQL injection
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

# check username and password against the ones from the configuration and sets logged_in key in session.
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

# remove key from session upon user logout. use pop() method and pass second parameter to it (the default) - deletes key from dictionary if present, or does nothing when key is not there. don't have to check if user was logged in.
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

# check to fire up server if we want to run this file as a standalone application
# if __name__ == '__main__':
#     app.run()


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

# TROUBLESHOOTING NOTE: if you get an exception later that a table cannot be found check that you did call the init_db function and that your table names are correct (singular vs. plural for example).

# after_request() functions are called after a request and passed the response that will be sent to the client. they have to return the response object or a different one. they are not guaranteed to be executed if an exception is raised - therefore better to use teardown_request().

# teardown_request() functions are not allowed to modify the request and their return values are ignored. if an exception occurred during the request, it is passed to each function; otherwise, None is passed in.

# special `g` object Flask provides to store current DB connection - stores info for one request only and is available from within each function. **never store DB connection in other objects - would not work with threaded environments.

# SECURITY NOTE: use question marks when building SQL statements (like with g.db.execute in add_entry() function). otherwise app will be vulnerable to SQL injection when using string formatting to build SQL statements.

# Jinja provides access to missing attributes and items of objects/dicts, even if there is no `logged_in` key in session.
# with Jinja, the `session` dict is available in the template - can use that to check if user is logged in or not



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

# Initialize DB connections before each request & shut them down afterwards.
# before_request() is called before a request and passed no arguments.
@app.before_request
def before_request():
    g.db = connect_db()

# teardown_request() gets called after the response has been constructed.
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
      db.close()

# show_entries() view function passes entries as dicts to the show_entries.html template and returns the rendered one.
@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

# add_entry() view function lets user add new entries if they are logged in with a form on the show_entries page. function only responds to POST requests.
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

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

# TROUBLESHOOTING NOTE: if you get an exception later that a table cannot be found check that you did call the init_db function and that your table names are correct (singular vs. plural for example).

# after_request() functions are called after a request and passed the response that will be sent to the client. they have to return the response object or a different one. they are not guaranteed to be executed if an exception is raised - therefore better to use teardown_request().

# teardown_request() functions are not allowed to modify the request and their return values are ignored. if an exception occurred during the request, it is passed to each function; otherwise, None is passed in.

# special `g` object Flask provides to store current DB connection - stores info for one request only and is available from within each function. **never store DB connection in other objects - would not work with threaded environments.

# SECURITY NOTE: use question marks when building SQL statements (like with g.db.execute in add_entry() function). otherwise app will be vulnerable to SQL injection when using string formatting to build SQL statements.



# Flask Tutorial: Flaskr App

My attempt to build the Flaskr app from the official Flask documentation tutorial.
http://flask.pocoo.org/docs/0.10/tutorial/#tutorial
https://github.com/mitsuhiko/flask/tree/master/examples/flaskr

_March 2015_

## Setting Up the Environment

* Utilizing Python 3.4.2.
* Install virtual environment in project root: `$ virtualenv venv`
* Activate virtual environment: `$ . venv/bin/activate`
* Install Flask 0.11.dev0 and its dependencies wtih: `$ pip install https://github.com/mitsuhiko/flask/tarball/master`
* Using Python's native sqlite3 module. Check for sqlite3:
```
$ python
Python 2.7.3 (default, Jan  2 2013, 16:53:07) 
[GCC 4.7.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import sqlite3
>>> sqlite3.version
'2.6.0'
>>> sqlite3.sqlite_version
'3.8.8.2'
```
* Create project directory
```
/flaskr
    /static
    /templates
```
## Objectives

1. Let the user sign in and out with credentials specified in the configuration. Only one user is supported.
2. When the user is logged in they can add new entries to the page consisting of a text-only title and some HTML for the text. This HTML is not sanitized because we trust the user here.
3. The page shows all entries so far in reverse order (newest on top) and the user can add new ones from there if logged in.

## Run App

1. Initialize database
```
$ flask --app=flaskr initdb
```
2. Run flaskr
```
$ flask --app=flaskr run
```


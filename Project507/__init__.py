"""
Initialization of a flask package
"""
from flask import Flask
import pathlib

# get the app variable
app = Flask(__name__)

# config the app
app.config['APPLICATION_ROOT'] = '/'
app.config['SECRET_KEY'] = b'$C\rE%}\xd6Z\x1d#].\x80\xb1;(\xd6v\xb5\x9d-h\xa22'
app.config['SESSION_COOKIE_NAME'] = 'login'
app.config['APPLICATION_ROOT'] = pathlib.Path(__file__).resolve().parent.parent
app.config['DATABASE_FILENAME'] = \
    app.config['APPLICATION_ROOT']/'var'/'movies.db'
app.config['TWITTER_CACHE'] = \
    app.config['APPLICATION_ROOT']/'var'/'twitter.json'
app.config['CURRENT_USER'] = None

# specify a route
import Project507.views
import Project507.db_config

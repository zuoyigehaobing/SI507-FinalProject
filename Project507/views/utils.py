import Project507
import sqlite3
import hashlib
from flask import session, flash, redirect, url_for
from functools import wraps


# decorator: login required in api
def login_required(func):
    """Decorate: login required in api."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        connection = Project507.db_config.get_db()
        logged_in_user = get_session_user(connection)
        if not logged_in_user:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_function


def get_session_user(connection=None):
    """Get the user in the session."""
    if Project507.app.config['CURRENT_USER'] is not None:
        session['username'] = Project507.app.config['CURRENT_USER']
    if 'username' not in session or session['username'] is None:
        session['username'] = None
        return None
    if connection:
        query = "SELECT * FROM users WHERE username=?"
        info = connection.execute(query, (session['username'], ))
        if len(info.fetchall()) == 0:
            session['username'] = None
    return session['username']

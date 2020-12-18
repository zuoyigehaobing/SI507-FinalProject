import Project507
import flask
import sqlite3


# Configure Dataset
def dict_factory(cursor, row):
    """To access the fetched data from the sqlite3 database as an dictionary"""
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """Open a new database connection. Enable foreign keys
    """
    if 'sqlite_db' not in flask.g:
        flask.g.sqlite_db = sqlite3.connect(
            str(Project507.app.config['DATABASE_FILENAME']))
        flask.g.sqlite_db.row_factory = dict_factory
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")
    return flask.g.sqlite_db


@Project507.app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request."""
    assert error or not error
    sqlite_db = flask.g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.commit()
        sqlite_db.close()

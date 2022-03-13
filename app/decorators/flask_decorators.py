from functools import wraps
from inspect import getframeinfo, currentframe

from flask import redirect, url_for, session

from pymysql import Error
from sqlalchemy.exc import OperationalError

from app.Database import DatabaseSession


# Make sure the user is logged in
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return decorated_function


# Make sure the user is logged in and is an admin
def admin_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        elif not session['is_admin']:
            return redirect(url_for('index'))
        else:
            return func(*args, **kwargs)

    return decorated_function


# Connect to the database and roll back commits when exceptions are thrown
def db_connector(f):
    def with_connection_(*args, **kwargs):
        with DatabaseSession() as conn:
            try:
                result = f(*args, connection=conn, **kwargs)
            except Error or OperationalError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + 'Line: ' +
                      str(getframeinfo(currentframe()).lineno) + '\n' + str(e))
                conn.rollback()
            except TypeError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + 'Line: ' +
                      str(getframeinfo(currentframe()).lineno) + '\n' + str(e) + '\n'
                      + 'Blank input detected, database not manipulated')
                conn.rollback()
            return result

    return with_connection_

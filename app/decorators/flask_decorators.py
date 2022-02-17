from functools import wraps
from flask import redirect, url_for, session


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

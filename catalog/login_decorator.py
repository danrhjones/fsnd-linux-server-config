from functools import wraps
from flask import g, request, redirect, url_for
from flask import session as login_session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            print request.url
            return redirect(url_for('showLogin'))
        return f(*args, **kwargs)
    return decorated_function

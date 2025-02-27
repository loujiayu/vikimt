from functools import wraps
from flask import session
from flask_login import current_user, login_required

def doctor_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'doctor':
            return {"error": "Doctor access required"}, 403
        return f(*args, **kwargs)
    return decorated_function

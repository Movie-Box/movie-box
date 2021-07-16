from functools import wraps
from flask_login import current_user
from app.models import User
from flask import flash, redirect, url_for, abort


def is_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.admin:
            abort(404)
        return func(*args, **kwargs)
    return decorated_function
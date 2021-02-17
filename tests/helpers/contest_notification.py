import logging
from functools import wraps


def contest_notification(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        new_instance = f(*args, **kwargs)

        return new_instance


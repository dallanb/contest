import logging
import traceback

from .events import *


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value
    if topic == 'contests':
        try:
            Contest().handle_event(key=key, data=data)
        except Exception:
            logging.error(traceback.format_exc())
            logging.error('Contest event err')
    elif topic == 'scores':
        try:
            Score().handle_event(key=key, data=data)
        except Exception:
            logging.error(traceback.format_exc())
            logging.error('Score event err')

from .events import *


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value
    if topic == 'contests':
        Contest().handle_event(key=key, data=data)
    elif topic == 'scores':
        Score().handle_event(key=key, data=data)

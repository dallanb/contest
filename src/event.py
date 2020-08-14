import json

from .services import Sport


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = json.loads(event.value)

    if topic == 'sports':
        Sport().handle_event(key=key, data=data)

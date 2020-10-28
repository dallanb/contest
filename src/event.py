import logging

from .services import ContestMaterialized


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value
    logging.info(key)
    if topic == 'contests':
        ContestMaterialized().handle_event(key=key, data=data)

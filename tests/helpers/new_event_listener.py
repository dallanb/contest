import logging

from src.events import Contest, Score


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value
    if topic == 'contests_test':
        try:
            Contest().handle_event(key=key, data=data)
        except Exception as ex:
            logging.error(ex)
            logging.error('contest error')
    if topic == 'scores_test':
        try:
            Score().handle_event(key=key, data=data)
        except Exception as ex:
            logging.error(ex)
            logging.error('score error')

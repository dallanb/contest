from . import app
from .events import *


def new_event_listener(event):
    with app.app_context():
        # start = time.perf_counter()
        topic = event.topic
        key = event.key
        data = event.value
        if topic == 'contests':
            Contest().handle_event(key=key, data=data)
        elif topic == 'scores':
            Score().handle_event(key=key, data=data)
        # finish = time.perf_counter()
        # logging.info(f'This is the total time taken {round(finish - start, 2)}')

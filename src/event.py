from flask import g

from . import Producer, app
from .events import *


def new_event_listener(event):
    with app.app_context():
        # start = time.perf_counter()
        topic = event.topic
        key = event.key
        g.producer = Producer(url=app.config['KAFKA_URL'])
        g.producer.start()
        # slower but safer
        while not g.producer.producer:
            pass
        data = event.value
        if topic == 'contests':
            Contest().handle_event(key=key, data=data)
        elif topic == 'scores':
            Score().handle_event(key=key, data=data)
        g.producer.stop()
        # finish = time.perf_counter()
        # logging.info(f'This is the total time taken {round(finish - start, 2)}')

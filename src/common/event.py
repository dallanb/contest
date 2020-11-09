from flask import g


class Event:
    @classmethod
    def _generate_endpoint(cls, topic, value):
        return {
            'endpoint': f"/{topic}/{str(value)}"
        }

    @classmethod
    def send(cls, topic, value, key):
        # this has to be done because the producer thread is only available to flask api request and not
        # internal requests made by the server so producer is being assigned globally in src/event.py and
        # src/__init__.py
        sender = None
        if g.producer and g.producer.producer:
            sender = g.producer
        if sender:
            sender.send(
                topic=topic,
                value=value,
                key=key
            )

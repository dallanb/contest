import logging

from flask import g


class Event:
    @classmethod
    def _generate_endpoint(cls, topic, value):
        return {
            'endpoint': f"/{topic}/{str(value)}"
        }

    @classmethod
    def send(cls, topic, value, key):
        if not g.producer.producer:
            logging.error('Cannot send kafka message because producer process is non-existent')
            return
        g.producer.send(
            topic=topic,
            value=value,
            key=key
        )

import logging

from .. import producer


class Event:
    @classmethod
    def _generate_endpoint(cls, topic, value):
        return {
            'endpoint': f"/{topic}/{str(value)}"
        }

    @classmethod
    def send(cls, topic, value, key):
        logging.info(producer)
        logging.info(producer.producer)
        if producer.producer:
            producer.send(
                topic=topic,
                value=value,
                key=key
            )

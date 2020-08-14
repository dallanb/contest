from flask import g
from kafka import KafkaProducer


class Producer:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=f"{g.config['KAFKA_HOST']}:{g.config['KAFKA_PORT']}")

    def send(self, **kwargs):
        self.producer.send(**kwargs)

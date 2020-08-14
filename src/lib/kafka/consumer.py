import multiprocessing

from flask import g
from kafka import KafkaConsumer


class Consumer(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=f"{g.config['KAFKA_HOST']}:{g.config['KAFKA_PORT']}")
        consumer.subscribe(g.config['KAFKA_TOPICS'])

        while not self.stop_event.is_set():
            for message in consumer:
                g.logger.info(message)
                if self.stop_event.is_set():
                    break

        consumer.close()

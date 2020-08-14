import multiprocessing

from flask import g
from kafka import KafkaConsumer


class Consumer(multiprocessing.Process):
    def __init__(self, host, port, topics):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        self.host = host
        self.port = port
        self.topics = topics

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=f"{self.host}:{self.port}")
        consumer.subscribe(self.topics)

        while not self.stop_event.is_set():
            for message in consumer:
                if self.stop_event.is_set():
                    break

        consumer.close()

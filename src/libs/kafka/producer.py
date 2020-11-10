import json
import threading
import time

from kafka import KafkaProducer


class Producer(threading.Thread):
    def __init__(self, url, acks=0):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.producer = None
        self.url = url
        self.acks = acks

    daemon = True

    def stop(self, timeout=None):
        self.producer.close(timeout)
        self.stop_event.set()

    def run(self):
        self.producer = KafkaProducer(bootstrap_servers=self.url, acks=self.acks, key_serializer=str.encode,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        while not self.stop_event.is_set():
            time.sleep(1)

        self.producer.close()
        self.producer = None

    def connected(self):
        if not self.producer:
            return False
        return self.producer.bootstrap_connected()

    def send(self, **kwargs):
        self.producer.send(**kwargs)

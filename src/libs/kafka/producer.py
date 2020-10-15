import json
import logging
import threading
import time

from kafka import KafkaProducer


class Producer(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.producer = None
        self.host = host
        self.port = port

    def stop(self):
        self.stop_event.set()

    def run(self):
        self.producer = KafkaProducer(bootstrap_servers=f"{self.host}:{self.port}", key_serializer=str.encode,
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
        logging.info("SENDING MESSAGE")
        self.producer.send(**kwargs)

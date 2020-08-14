import threading, time

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
        self.producer = None

    def run(self):
        self.producer = KafkaProducer(bootstrap_servers=f"{self.host}:{self.port}")

        while not self.stop_event.is_set():
            time.sleep(1)

        self.producer.close()

    def send(self, **kwargs):
        if self.producer:
            self.producer.send(**kwargs)

import logging
import time
from datetime import datetime

from src import Producer, Contest, app


# delta is in days
def check_contest_timeout(delta):
    logging.info('checking contest timeout')
    current_time = datetime.now()
    expiry_time = current_time + delta

    timestamp = int(datetime.timestamp(current_time) * 1000)
    expiry_timestamp = int(datetime.timestamp(expiry_time) * 1000)

    contests = Contest.query.filter(Contest.start_time > timestamp, Contest.start_time < expiry_timestamp).all()

    # eventually attempt to run multiple threads in parallel?
    producer = Producer(url=app.config['KAFKA_URL'])
    producer.start()

    connected = producer.connected()
    while not connected:
        logging.info('Connecting...')
        time.sleep(1)
        connected = producer.connected()

    for contest in contests:
        producer.send(
            topic='contests',
            key='contest_timeout',
            value={
                'uuid': str(contest.uuid)
            }
        )

    producer.stop()

    logging.info("done checking contest timeout")
    return

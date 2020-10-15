import logging
import time
from datetime import datetime

from src import Producer, Contest, app


# delta is in minutes
def check_contest_timeout(delta):
    logging.info('checking contest timeout')
    expiry_time = datetime.now() + delta
    timestamp = int(datetime.timestamp(expiry_time) * 1000)

    contests = Contest.query.filter(Contest.start_time < timestamp).all()

    # eventually attempt to run multiple threads in parallel?
    producer = Producer(host=app.config['KAFKA_HOST'], port=app.config['KAFKA_PORT'])
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

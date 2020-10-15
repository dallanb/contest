import logging
from datetime import datetime

from flask import g


# delta is in minutes
def check_contest_timeout(delta):
    logging.info('checking contest timeout')
    expiry_time = datetime.now() + delta
    timestamp = int(datetime.timestamp(expiry_time) * 1000)

    Contest = g.src.Contest

    contests = Contest.query.filter(Contest.start_time < timestamp)
    logging.info(contests)

    return

import logging
import time
from datetime import datetime

from src import Contest, ContestService
# delta is in days
from src.common import ContestStatusEnum

contest_service = ContestService()


def check_contest_active(delta):
    logging.info('checking contest active')
    current_time = datetime.now()
    expiry_time = current_time + delta

    timestamp = int(datetime.timestamp(current_time) * 1000)
    expiry_timestamp = int(datetime.timestamp(expiry_time) * 1000)

    contests = contest_service.contest_model.query.filter(Contest.start_time > timestamp,
                                                          Contest.start_time < expiry_timestamp).all()

    for contest in contests:
        if ContestStatusEnum[contest.status.name] == ContestStatusEnum['ready']:
            contest_service.apply(instance=contest, status=ContestStatusEnum.active.name)

    time.sleep(1)
    logging.info("done checking contest active")
    return

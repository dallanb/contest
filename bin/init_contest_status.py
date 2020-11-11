import logging

from src import ContestStatus, db


def init_contest_status(status_enums):
    logging.info(f"init_contest_status started")

    for status_enum in status_enums:
        status = ContestStatus(name=status_enum)
        db.session.add(status)
    db.session.commit()
    logging.info(f"init_contest_status completed")
    return

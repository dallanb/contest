from flask import g
import logging


def init_contest_status(status_enums):
    logging.info(f"init_contest_status started")
    ContestStatus = g.src.ContestStatus

    for status_enum in status_enums:
        status = ContestStatus(name=status_enum)
        g.src.db.session.add(status)
    g.src.db.session.commit()
    logging.info(f"init_contest_status completed")
    return

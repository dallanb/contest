import datetime
import os

from flask import g
from flask.cli import FlaskGroup

import src
from bin import init_participant_status, init_contest_status, check_contest_timeout
from src import app, db, common

cli = FlaskGroup(app)


def full_init():
    initialize_statuses()
    os.system('flask seed run')


def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


def clear_db():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()


def clear_cache():
    common.cache.clear()


def initialize_statuses():
    with app.app_context():
        g.src = src
        init_contest_status(status_enums=common.ContestStatusEnum)
        init_participant_status(status_enums=common.ParticipantStatusEnum)
        return


def check_timeouts():
    delta = datetime.timedelta(days=1)
    check_contest_timeout(delta=delta)


@cli.command("init")
def init():
    full_init()


@cli.command("reset_db")
def reset_db():
    create_db()


@cli.command("delete_db")
def delete_db():
    clear_db()


@cli.command("flush_cache")
def flush_cache():
    clear_cache()


@cli.command("init_status")
def init_status():
    initialize_statuses()


@cli.command("check_timeout")
def check_timeout():
    check_timeouts()


# @cli.command("stop_kafka")
# def stop_kafka():


if __name__ == "__main__":
    cli()

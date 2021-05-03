import datetime
import os

from flask.cli import FlaskGroup

from bin import init_participant_status, init_contest_status, check_contest_active
from src import app, db, common

cli = FlaskGroup(app)


def full_load():
    initialize_statuses()
    os.system('flask seed run')


def init_db():
    db.drop_all()
    db.configure_mappers()
    db.create_all()
    db.session.commit()


def drop_db():
    db.drop_all()
    db.session.commit()


def configure_db():
    db.configure_mappers()
    db.session.commit()


def create_db():
    db.create_all()
    db.session.commit()


def reset_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


def clear_db():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()


def clear_cache():
    common.cache.cache.clear()


def initialize_statuses():
    init_contest_status(status_enums=common.ContestStatusEnum)
    init_participant_status(status_enums=common.ParticipantStatusEnum)
    return


def check_actives():
    delta = datetime.timedelta(days=1)
    check_contest_active(delta=delta)


@cli.command("init")
def init():
    init_db()


@cli.command("load")
def load():
    full_load()


@cli.command("create")
def create():
    create_db()


@cli.command("drop")
def drop():
    drop_db()


@cli.command("reset")
def reset():
    reset_db()


@cli.command("configure")
def configure():
    configure_db()


@cli.command("delete")
def delete():
    clear_db()


@cli.command("flush_cache")
def flush_cache():
    clear_cache()


@cli.command("load_status")
def load_status():
    initialize_statuses()


@cli.command("check_active")
def check_active():
    check_actives()


if __name__ == "__main__":
    cli()

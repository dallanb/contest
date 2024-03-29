import pytest

from bin import init_contest_status, init_participant_status
from src import db, common


@pytest.fixture(scope='function')
def reset_db():
    # delete
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
    # create
    db.create_all()
    db.session.commit()
    # load
    init_contest_status(status_enums=common.ContestStatusEnum)
    init_participant_status(status_enums=common.ParticipantStatusEnum)

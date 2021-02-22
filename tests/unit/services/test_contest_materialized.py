import pytest

from src import services, ManualException
from src.common import ParticipantStatusEnum, time_now
from tests.helpers import generate_uuid

contest_service = services.ContestMaterializedService()


###########
# Find
###########
def test_contest_find(reset_db, pause_notification, seed_contest, seed_contest_materialized):
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called
    THEN it should return 1 contest
    """

    contests = contest_service.find()
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.uuid == pytest.contest.uuid


def test_contest_find_by_uuid():
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 contest
    """
    contest = pytest.contest
    uuid = contest.uuid

    contests = contest_service.find(uuid=uuid)
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.uuid == uuid


def test_contest_find_by_league():
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with league
    THEN it should return 1 contest
    """
    contest = pytest.contest
    league_uuid = contest.league_uuid

    contests = contest_service.find(league=league_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.league == league_uuid


def test_contest_find_by_non_existent_column():
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 contest and ManualException with code 400
    """
    try:
        _ = contest_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_contest_create(reset_db, pause_notification, seed_contest, mock_fetch_member_user, mock_fetch_location):
    """
    GIVEN 0 contest instance in the database
    WHEN the create method is called
    THEN it should return 1 contest and add 1 contest instance into the database
    """
    owner = services.ParticipantService().fetch_member_user(user_uuid=str(pytest.owner_user_uuid),
                                                            league_uuid=str(pytest.league_uuid))
    location = services.ContestService().fetch_location(uuid=str(pytest.location_uuid))
    contest = contest_service.create(
        uuid=pytest.contest.uuid, name=pytest.name, status=pytest.contest.status.name,
        start_time=pytest.start_time,
        owner=pytest.owner_user_uuid, location=location.get('name', ''), league=pytest.league_uuid,
        participants={str(owner.get('uuid', '')): {
            'member_uuid': str(owner.get('uuid', '')),
            'display_name': owner.get('display_name', ''),
            'status': ParticipantStatusEnum['active'].name,
            'score': None,
            'strokes': None,
        }})

    assert contest.uuid == pytest.contest.uuid


###########
# Update
###########
def test_contest_update(reset_db, pause_notification, seed_contest, seed_contest_materialized):
    """
    GIVEN 1 contest instance in the database
    WHEN the update method is called
    THEN it should return 1 contest and update 1 contest instance into the database
    """
    contest = contest_service.update(uuid=pytest.contest.uuid, start_time=time_now() + 10000)
    assert contest.uuid is not None

    contests = contest_service.find(uuid=contest.uuid)
    assert contests.total == 1
    assert len(contests.items) == 1


###########
# Apply
###########
def test_contest_apply(reset_db, pause_notification, seed_contest, seed_contest_materialized):
    """
    GIVEN 1 contest instance in the database
    WHEN the apply method is called
    THEN it should return 1 contest and update 1 contest instance in the database
    """
    contest = contest_service.apply(instance=pytest.contest, start_time=time_now() + 10000)
    assert contest.uuid is not None

    contests = contest_service.find(uuid=contest.uuid)
    assert contests.total == 1
    assert len(contests.items) == 1

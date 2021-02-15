import pytest

from src import services, ManualException
from tests.helpers import generate_uuid

global_contest = None
contest_service = services.ContestService()


###########
# Find
###########
def test_contest_find(reset_db, seed_contest):
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


def test_contest_find_by_league_uuid():
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with league_uuid
    THEN it should return 1 contest
    """
    contest = pytest.contest
    league_uuid = contest.league_uuid

    contests = contest_service.find(league_uuid=league_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.league_uuid == league_uuid


def test_contest_find_by_location_uuid():
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with location_uuid
    THEN it should return 1 contest
    """
    contest = pytest.contest
    location_uuid = contest.location_uuid

    contests = contest_service.find(location_uuid=location_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.location_uuid == location_uuid


def test_contest_find_include_participants(seed_participant):
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with include argument to also return participants
    THEN it should return 1 contest
    """
    contest = pytest.contest

    contests = contest_service.find(include=['participants'])
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert len(contest.participants) == 1


def test_contest_find_include_avatar(seed_avatar):
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with include argument to also return avatar
    THEN it should return 1 contest
    """
    contests = contest_service.find(include=['avatar'])
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.avatar is not None


def test_contest_find_include_sport(seed_sport):
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with include argument to also return sport
    THEN it should return 1 contest
    """
    contests = contest_service.find(include=['sport'])
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.sport is not None


def test_contest_find_include_participants_include_avatar_include_sport():
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with include argument to also return sport, participants and avatar
    THEN it should return 1 contest
    """
    contests = contest_service.find(include=['sport', 'participants', 'avatar'])
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert len(contest.participants) == 1
    assert contest.avatar is not None
    assert contest.sport is not None


def test_contest_find_w_pagination(seed_contest):
    """
    GIVEN 2 contest instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of contests defined in the pagination arguments
    """
    contests_0 = contest_service.find(page=1, per_page=1)
    assert contests_0.total == 2
    assert len(contests_0.items) == 1

    contests_1 = contest_service.find(page=2, per_page=1)
    assert contests_1.total == 2
    assert len(contests_1.items) == 1
    assert contests_1.items[0] != contests_0.items[0]

    contests = contest_service.find(page=1, per_page=2)
    assert contests.total == 2
    assert len(contests.items) == 2


def test_contest_find_w_bad_pagination():
    """
    GIVEN 2 contest instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 contest
    """
    contests = contest_service.find(page=3, per_page=3)
    assert contests.total == 2
    assert len(contests.items) == 0


def test_contest_find_by_league_uuid_none_found():
    """
    GIVEN 2 contest instance in the database
    WHEN the find method is called with a random league_uuid
    THEN it should return the 0 contest
    """
    contests = contest_service.find(league_uuid=generate_uuid())
    assert contests.total == 0
    assert len(contests.items) == 0


def test_contest_find_by_non_existent_column():
    """
    GIVEN 2 contest instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 contest and ManualException with code 400
    """
    try:
        _ = contest_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_contest_find_by_non_existent_include():
    """
    GIVEN 2 contest instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 contest and ManualException with code 400
    """
    try:
        _ = contest_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_contest_find_by_non_existent_expand():
    """
    GIVEN 2 contest instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 contest and ManualException with code 400
    """
    try:
        _ = contest_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_contest_create(reset_db):
    """
    GIVEN 0 contest instance in the database
    WHEN the create method is called
    THEN it should return 1 contest and add 1 contest instance into the database
    """
    contest = contest_service.create(status='pending', owner_uuid=pytest.owner_user_uuid, name=pytest.name,
                                     start_time=pytest.start_time, location_uuid=pytest.location_uuid,
                                     league_uuid=pytest.league_uuid)

    assert contest.uuid is not None
    assert contest.owner_uuid == pytest.owner_user_uuid


def test_contest_create_dup(reset_db):
    """
    GIVEN 1 contest instance in the database
    WHEN the create method is called with the exact same parameters of an existing contest
    THEN it should return 1 contest and add 1 contest instance into the database
    """
    contest = contest_service.create(status='pending', owner_uuid=pytest.owner_user_uuid, name=pytest.name,
                                     start_time=pytest.start_time, location_uuid=pytest.location_uuid,
                                     league_uuid=pytest.league_uuid)

    assert contest.uuid is not None
    assert contest.owner_uuid == pytest.owner_user_uuid


def test_contest_create_w_bad_field():
    """
    GIVEN 2 contest instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 contest and add 0 contest instance into the database and ManualException with code 500
    """
    try:
        _ = contest_service.create(status='pending', owner_uuid=pytest.owner_user_uuid, name=pytest.name,
                                   start_time=pytest.start_time, location_uuid=pytest.location_uuid,
                                   league_uuid=pytest.league_uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Init
###########
def test_contest_init(reset_db):
    """
    GIVEN 0 contest instance in the database
    WHEN the init method is called
    THEN it should return 1 contest and add 0 contest instance into the database
    """
    contest = contest_service.init(status='pending', owner_uuid=pytest.owner_user_uuid, name=pytest.name,
                                   start_time=pytest.start_time, location_uuid=pytest.location_uuid,
                                   league_uuid=pytest.league_uuid, )
    assert contest.uuid is not None

    contests = contest_service.find(uuid=contest.uuid)
    assert contests.total == 0
    assert len(contests.items) == 0


def test_contest_init_dup(seed_contest):
    """
    GIVEN 1 contest instance in the database
    WHEN the init method is called with duplicate member_uuid and duplicate party
    THEN it should return 1 contest and init 0 contest instance into the database
    """

    contests = contest_service.find()
    assert contests.total == 1
    assert len(contests.items) == 1

    contest = contest_service.init(status='pending', owner_uuid=pytest.owner_user_uuid, name=pytest.name,
                                   start_time=pytest.start_time, location_uuid=pytest.location_uuid,
                                   league_uuid=pytest.league_uuid)
    assert contest.uuid is not None
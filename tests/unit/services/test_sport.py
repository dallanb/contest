import logging

import pytest

from src import services, ManualException
from tests.helpers import generate_uuid

sport_service = services.SportService()


###########
# Find
###########
def test_sport_find(reset_db, pause_notification, seed_contest, seed_sport):
    """
    GIVEN 1 sport instance in the database
    WHEN the find method is called
    THEN it should return 1 sport
    """
    sports = sport_service.find()

    assert sports.total == 1
    assert len(sports.items) == 1


def test_sport_find_by_uuid():
    """
    GIVEN 1 sport instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 sport
    """

    sports = sport_service.find(uuid=pytest.sport.uuid)

    assert sports.total == 1
    assert len(sports.items) == 1
    sport = sports.items[0]
    assert sport.uuid == pytest.sport.uuid


def test_sport_find_expand_contest():
    """
    GIVEN 1 sport instance in the database
    WHEN the find method is called with uuid and with expand argument to also return contest
    THEN it should return 1 sport
    """

    sports = sport_service.find(uuid=pytest.sport.uuid, expand=['contest'])

    assert sports.total == 1
    assert len(sports.items) == 1
    sport = sports.items[0]
    assert sport.contest is not None
    assert sport.contest.uuid is not None


def test_sport_find_by_contest_uuid():
    """
    GIVEN 1 sport instance in the database
    WHEN the find method is called with contest_uuid
    THEN it should return as many sport exist for that contest_uuid
    """

    sports = sport_service.find(contest_uuid=pytest.contest.uuid)

    assert sports.total == 1
    assert len(sports.items) == 1


def test_sport_find_w_pagination(pause_notification, seed_contest, seed_sport):
    """
    GIVEN 2 sport instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of sports defined in the pagination arguments
    """
    sports_0 = sport_service.find(page=1, per_page=1)
    assert sports_0.total == 2
    assert len(sports_0.items) == 1

    sports_1 = sport_service.find(page=2, per_page=1)
    assert sports_1.total == 2
    assert len(sports_1.items) == 1
    assert sports_1.items[0] != sports_0.items[0]

    sports = sport_service.find(page=1, per_page=2)
    assert sports.total == 2
    assert len(sports.items) == 2


def test_sport_find_w_bad_pagination():
    """
    GIVEN 2 sport instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 sport
    """
    sports = sport_service.find(page=3, per_page=3)
    assert sports.total == 2
    assert len(sports.items) == 0


def test_sport_find_by_non_existent_column():
    """
    GIVEN 2 sport instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 sport and ManualException with code 400
    """
    try:
        _ = sport_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_sport_find_by_non_existent_include():
    """
    GIVEN 2 sport instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 sport and ManualException with code 400
    """
    try:
        _ = sport_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_sport_find_by_non_existent_expand():
    """
    GIVEN 2 sport instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 sport and ManualException with code 400
    """
    try:
        _ = sport_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_sport_create(reset_db, pause_notification, seed_contest):
    """
    GIVEN 0 sport instance in the database
    WHEN the create method is called
    THEN it should return 1 sport and add 1 sport instance into the database
    """

    sport = sport_service.create(sport_uuid=pytest.sport_uuid, contest=pytest.contest)
    assert sport.uuid is not None
    assert sport.contest is not None


def test_sport_create_dup_contest(pause_notification):
    """
    GIVEN 1 sport instance in the database
    WHEN the create method is called with duplicate contest
    THEN it should return 0 sport and add 0 sport instance into the database and ManualException with code 500
    """

    try:
        _ = sport_service.create(sport_uuid=pytest.sport_uuid, contest=pytest.contest)
    except ManualException as ex:
        assert ex.code == 500


def test_sport_create_wo_contest(pause_notification):
    """
    GIVEN 1 sport instance in the database
    WHEN the create method is called without contest
    THEN it should return 0 sport and add 0 sport instance into the database and ManualException with code 500
    """

    try:
        _ = sport_service.create(sport_uuid=pytest.sport_uuid)
    except ManualException as ex:
        assert ex.code == 500


def test_sport_create_w_non_existent_contest_uuid(pause_notification):
    """
    GIVEN 1 sport instance in the database
    WHEN the create method is called with non existent contest uuid
    THEN it should return 0 sport and add 0 sport instance into the database and ManualException with code 500
    """

    try:
        _ = sport_service.create(sport_uuid=pytest.sport_uuid, contest_uuid=generate_uuid())
    except ManualException as ex:
        assert ex.code == 500


def test_sport_create_w_bad_field(reset_db, pause_notification, seed_contest):
    """
    GIVEN 0 sport instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 sport and add 0 sport instance into the database and ManualException with code 500
    """

    try:
        _ = sport_service.create(sport_uuid=pytest.sport_uuid, contest=pytest.contest, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Init
###########
def test_sport_init(reset_db, pause_notification, seed_contest):
    """
    GIVEN 0 sport instance in the database
    WHEN the init method is called
    THEN it should return 1 sport and add 0 sport instance into the database
    """

    sport = sport_service.init(sport_uuid=pytest.sport_uuid, contest=pytest.contest)
    assert sport.uuid is not None

    # since sport is init is associated with contest it will be inserted into the db on find
    sports = sport_service.find(uuid=sport.uuid)
    assert sports.total == 1
    assert len(sports.items) == 1


def test_sport_init_dup(pause_notification):
    """
    GIVEN 1 sport instance in the database
    WHEN the init method is called with duplicate member_uuid and duplicate party
    THEN it should return 1 sport and init 0 sport instance into the database
    """

    sports = sport_service.find()
    assert sports.total == 1
    assert len(sports.items) == 1

    sport = sport_service.init(sport_uuid=pytest.sport_uuid, contest=pytest.contest)
    assert sport.uuid is not None
    sport_service._rollback()


def test_sport_init_w_bad_sport_uuid(reset_db, pause_notification, seed_contest):
    """
    GIVEN 0 sport instance in the database
    WHEN the init method is called with a bad sport_uuid
    THEN it should return 1 sport and add 0 sport instance into the database
    """
    sport = sport_service.init(sport_uuid=1, contest=pytest.contest)
    assert sport.uuid is not None

    # since we have linked the sport instance to an existing contest instance, the find operation will commit
    # it to the db
    try:
        _ = sport_service.find(uuid=sport.uuid)
    except ManualException as ex:
        assert ex.code == 400

    # this is fine because it is not actually being committed to the database
    sport = sport_service.init(sport_uuid=1)
    assert sport.uuid is not None
    sport_service._rollback()


def test_sport_init_w_bad_field(reset_db, pause_notification, seed_contest):
    """
    GIVEN 0 sport instance in the database
    WHEN the init method is called with a bad field
    THEN it should return 1 sport and add 0 sport instance into the database and ManualException with code 500
    """
    try:
        _ = sport_service.init(sport_uuid=pytest.sport_uuid, contest=pytest.contest,
                               junk='junk')
    except ManualException as ex:
        assert ex.code == 500

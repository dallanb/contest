import time

import pytest

from src import services, ManualException
from src.common import time_now
from tests.helpers import generate_uuid

global_contest = None
contest_service = services.ContestService()


###########
# Find
###########
def test_contest_find(reset_db, pause_notification, seed_contest):
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


def test_contest_find_include_participants(pause_notification, seed_participant):
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


def test_contest_find_w_pagination(pause_notification, seed_contest):
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
def test_contest_create(reset_db, pause_notification):
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


def test_contest_create_dup(pause_notification):
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


def test_contest_create_w_bad_field(pause_notification):
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


def test_contest_init_dup(pause_notification, seed_contest):
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


def test_contest_init_w_bad_league_uuid(reset_db):
    """
    GIVEN 0 contest instance in the database
    WHEN the init method is called with a bad league_uuid
    THEN it should return 1 contest and add 0 contest instance into the database
    """
    contest = contest_service.init(status='pending', owner_uuid=pytest.owner_user_uuid, name=pytest.name,
                                   start_time=pytest.start_time, location_uuid=pytest.location_uuid,
                                   league_uuid=1)
    assert contest.uuid is not None

    contests = contest_service.find(uuid=contest.uuid)
    assert contests.total == 0
    assert len(contests.items) == 0


def test_contest_init_w_bad_field(reset_db):
    """
    GIVEN 0 contest instance in the database
    WHEN the init method is called with a bad league_uuid
    THEN it should return 1 contest and add 0 contest instance into the database and ManualException with code 500
    """
    try:
        _ = contest_service.init(status='pending', owner_uuid=pytest.owner_user_uuid, name=pytest.name,
                                 start_time=pytest.start_time, location_uuid=pytest.location_uuid,
                                 league_uuid=pytest.league_uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_contest_update(reset_db, pause_notification, seed_contest):
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


def test_contest_update_w_bad_uuid(reset_db, pause_notification, seed_contest):
    """
    GIVEN 1 contest instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 contest and update 0 contest instance into the database and ManualException with code 404
    """
    try:
        _ = contest_service.update(uuid=generate_uuid(), start_time=time_now() + 10000)
    except ManualException as ex:
        assert ex.code == 404


def test_contest_update_w_bad_field(pause_notification):
    """
    GIVEN 1 contest instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 contest and update 0 contest instance in the database and ManualException with code 400
    """
    try:
        _ = contest_service.update(uuid=pytest.contest.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_contest_apply(reset_db, pause_notification, seed_contest):
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


def test_contest_apply_w_bad_contest(reset_db, pause_notification, seed_contest):
    """
    GIVEN 1 contest instance in the database
    WHEN the apply method is called with random uuid
    THEN it should return 0 contest and update 0 contest instance in the database and ManualException with code 404
    """
    try:
        _ = contest_service.apply(instance=generate_uuid(), start_time=time_now() + 10000)
    except ManualException as ex:
        assert ex.code == 400


def test_contest_apply_w_bad_field(pause_notification):
    """
    GIVEN 1 contest instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 contest and update 0 contest instance in the database and ManualException with code 400
    """
    try:
        _ = contest_service.apply(instance=pytest.contest, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Misc
###########
def test_check_contest_status(reset_db, pause_notification,
                              seed_contest, seed_owner,
                              seed_participant):
    """
    GIVEN 1 pending contest instance, 1 active owner participant instance and 1 active participant instance in the database
    WHEN the check_contest_status method is called
    THEN it should update the contest status from 'pending' to 'ready'
    """
    assert pytest.contest.status.name == 'pending'
    assert len(pytest.contest.participants) == 2

    services.ParticipantService().apply(instance=pytest.participant, status='active')
    assert pytest.contest.status.name == 'pending'
    for participant in pytest.contest.participants:
        assert participant.status.name == 'active'

    contest_service.check_contest_status(uuid=pytest.contest.uuid)
    assert pytest.contest.status.name == 'ready'


def test_check_contest_status_no_change(reset_db, pause_notification, seed_contest, seed_owner,
                                        seed_participant):
    """
    GIVEN 1 pending contest instance, 1 active owner participant instance and 1 pending participant instance in the database
    WHEN the check_contest_status method is called
    THEN it should not change the contest status
    """
    assert pytest.contest.status.name == 'pending'
    assert len(pytest.contest.participants) == 2

    contest_service.check_contest_status(uuid=pytest.contest.uuid)
    assert pytest.contest.status.name == 'pending'


def test_check_contest_status_active(reset_db, pause_notification,
                                     seed_contest, seed_owner,
                                     seed_participant):
    """
    GIVEN 1 active contest instance, 1 completed owner participant instance and 1 completed participant instance in the database
    WHEN the check_contest_status method is called
    THEN it should update the contest status from 'active' to 'completed'
    """
    services.ParticipantService().apply(instance=pytest.participant, status='active')
    contest_service.check_contest_status(uuid=pytest.contest.uuid)
    assert pytest.contest.status.name == 'ready'

    services.ContestService().apply(instance=pytest.contest, status='active')
    assert pytest.contest.status.name == 'active'

    services.ParticipantService().apply(instance=pytest.participant, status='completed')
    services.ParticipantService().apply(instance=pytest.owner, status='completed')
    assert pytest.contest.status.name == 'active'

    contest_service.check_contest_status(uuid=pytest.contest.uuid)
    assert pytest.contest.status.name == 'completed'


def test_check_contest_status_participant_inactive_owner_active(reset_db, pause_notification,
                                                                seed_contest, seed_owner,
                                                                seed_participant):
    """
    GIVEN 1 pending contest instance, 1 active owner participant instance and 1 inactive participant instance in the database
    WHEN the check_contest_status method is called
    THEN it should update the contest status from 'pending' to 'inactive'
    """
    services.ParticipantService().apply(instance=pytest.participant, status='inactive')
    contest_service.check_contest_status(uuid=pytest.contest.uuid)
    assert pytest.contest.status.name == 'inactive'


def test_check_contest_status_participant_inactive_participant_active_owner_active(reset_db, pause_notification,
                                                                                   seed_contest, seed_owner,
                                                                                   seed_participant):
    """
    GIVEN 1 pending contest instance, 1 active owner participant instance, 1 active participant instance and 1 inactive participant instance in the database
    WHEN the check_contest_status method is called
    THEN it should update the contest status from 'pending' to 'ready'
    """
    new_participant = services.ParticipantService().create(status='pending',
                                                           member_uuid=generate_uuid(),
                                                           contest=pytest.contest)
    services.ParticipantService().apply(instance=pytest.participant, status='inactive')
    contest_service.check_contest_status(uuid=pytest.contest.uuid)
    # we still have one participant that is unaccounted for
    assert pytest.contest.status.name == 'pending'

    services.ParticipantService().apply(instance=new_participant, status='active')
    contest_service.check_contest_status(uuid=pytest.contest.uuid)
    assert pytest.contest.status.name == 'ready'


def test_check_contest_status_participants_inactive_owner_active(reset_db, pause_notification,
                                                                 seed_contest, seed_owner,
                                                                 seed_participant):
    """
    GIVEN 1 pending contest instance, 1 active owner participant instance, 2 inactive participant instance in the database
    WHEN the check_contest_status method is called
    THEN it should update the contest status from 'pending' to 'inactive'
    """
    new_participant = services.ParticipantService().create(status='pending',
                                                           member_uuid=generate_uuid(),
                                                           contest=pytest.contest)
    services.ParticipantService().apply(instance=pytest.participant, status='inactive')
    contest_service.check_contest_status(uuid=pytest.contest.uuid)
    # we still have one participant that is unaccounted for
    assert pytest.contest.status.name == 'pending'

    services.ParticipantService().apply(instance=new_participant, status='inactive')
    contest_service.check_contest_status(uuid=pytest.contest.uuid)
    assert pytest.contest.status.name == 'inactive'


def test_fetch_location(reset_db, pause_notification, mock_fetch_location):
    """
    GIVEN 0 contest instance in the database
    WHEN the fetch_location method is called
    THEN it should return a location
    """
    location_uuid = str(pytest.location_uuid)
    location = contest_service.fetch_location(uuid=location_uuid)
    assert location['uuid'] == location_uuid


def test_fetch_location_bad_uuid(reset_db, pause_notification, mock_fetch_location):
    """
    GIVEN 0 contest instance in the database
    WHEN the fetch_location method is called with an invalid uuid
    THEN it should return None
    """
    location_uuid = str(generate_uuid())
    location = contest_service.fetch_location(uuid=location_uuid)
    assert location is None


def test_find_by_start_time_range(reset_db, pause_notification, seed_contest):
    """
    GIVEN 1 contest instance in the database
    WHEN the find_by_start_time_range method is called
    THEN it should return 1 contest
    """
    start_time = pytest.start_time
    struct = time.gmtime(start_time / 1000)
    year = struct[0]
    month = struct[1]
    contests = contest_service.find_by_start_time_range(month=month, year=year)
    assert contests.total == 1


def test_find_by_start_time_range_bad_uuid():
    """
    GIVEN 1 contest instance in the database
    WHEN the find_by_start_time_range method is called with an future month and year
    THEN it should return 0 contest
    """
    start_time = pytest.start_time
    struct = time.gmtime(start_time / 1000)
    year = struct[0] + 1
    month = struct[1]
    contests = contest_service.find_by_start_time_range(month=month, year=year)
    assert contests.total == 0

import logging
import time

import pytest

from src import services, ManualException
from src.common import time_now
from tests.helpers import generate_uuid

participant_service = services.ParticipantService()


###########
# Find
###########
def test_participant_find(reset_db, pause_notification, seed_contest, seed_owner):
    """
    GIVEN 1 participant instance in the database
    WHEN the find method is called
    THEN it should return 1 participant
    """

    participants = participant_service.find()
    assert participants.total == 1
    assert len(participants.items) == 1
    participant = participants.items[0]
    assert participant.uuid == pytest.owner.uuid


def test_participant_find_by_uuid():
    """
    GIVEN 1 participant instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 participant
    """
    participant = pytest.owner
    uuid = participant.uuid

    participants = participant_service.find(uuid=uuid)
    assert participants.total == 1
    assert len(participants.items) == 1
    participant = participants.items[0]
    assert participant.uuid == uuid


def test_participant_find_by_member_uuid():
    """
    GIVEN 1 participant instance in the database
    WHEN the find method is called with member_uuid
    THEN it should return 1 participant
    """
    participant = pytest.owner
    member_uuid = participant.member_uuid

    participants = participant_service.find(member_uuid=member_uuid)
    assert participants.total == 1
    assert len(participants.items) == 1
    participant = participants.items[0]
    assert participant.member_uuid == member_uuid


def test_participant_find_by_contest_uuid():
    """
    GIVEN 1 participant instance in the database
    WHEN the find method is called with contest_uuid
    THEN it should return 1 participant
    """
    participant = pytest.owner
    contest_uuid = participant.contest_uuid

    participants = participant_service.find(contest_uuid=contest_uuid)
    assert participants.total == 1
    assert len(participants.items) == 1
    participant = participants.items[0]
    assert participant.contest_uuid == contest_uuid


def test_participant_find_expand_contest():
    """
    GIVEN 1 participant instance in the database
    WHEN the find method is called with expand argument to also return contest
    THEN it should return 1 participant
    """
    participants = participant_service.find(expand=['contest'])
    assert participants.total == 1
    assert len(participants.items) == 1
    participant = participants.items[0]
    assert participant.contest.uuid is not None


def test_participant_find_w_pagination(pause_notification, seed_participant):
    """
    GIVEN 2 participant instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of participants defined in the pagination arguments
    """
    participants_0 = participant_service.find(page=1, per_page=1)
    assert participants_0.total == 2
    assert len(participants_0.items) == 1

    participants_1 = participant_service.find(page=2, per_page=1)
    assert participants_1.total == 2
    assert len(participants_1.items) == 1
    assert participants_1.items[0] != participants_0.items[0]

    participants = participant_service.find(page=1, per_page=2)
    assert participants.total == 2
    assert len(participants.items) == 2


def test_participant_find_w_bad_pagination():
    """
    GIVEN 2 participant instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 participant
    """
    participants = participant_service.find(page=3, per_page=3)
    assert participants.total == 2
    assert len(participants.items) == 0


def test_participant_find_by_member_uuid_none_found():
    """
    GIVEN 2 participant instance in the database
    WHEN the find method is called with a random member_uuid
    THEN it should return the 0 participant
    """
    participants = participant_service.find(member_uuid=generate_uuid())
    assert participants.total == 0
    assert len(participants.items) == 0


def test_participant_find_by_non_existent_column():
    """
    GIVEN 2 participant instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 participant and ManualException with code 400
    """
    try:
        _ = participant_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_participant_find_by_non_existent_include():
    """
    GIVEN 2 participant instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 participant and ManualException with code 400
    """
    try:
        _ = participant_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_participant_find_by_non_existent_expand():
    """
    GIVEN 2 participant instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 participant and ManualException with code 400
    """
    try:
        _ = participant_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_participant_create(reset_db, pause_notification, seed_contest, seed_owner):
    """
    GIVEN 1 participant instance in the database
    WHEN the create method is called
    THEN it should return 1 participant and add 1 participant instance into the database
    """
    participant = participant_service.create(status='active', member_uuid=pytest.participant_member_uuid,
                                             contest=pytest.contest)

    assert participant.uuid is not None
    assert participant.member_uuid == pytest.participant_member_uuid


def test_participant_create_dup(pause_notification):
    """
    GIVEN 2 participant instance in the database
    WHEN the create method is called with the exact same parameters of an existing participant
    THEN it should return 0 participant and add 0 participant instance into the database and ManualException with code 500
    """
    try:
        _ = participant_service.create(status='pending', member_uuid=pytest.owner_member_uuid,
                                       contest=pytest.contest)
    except ManualException as ex:
        assert ex.code == 500


def test_participant_create_w_bad_field(pause_notification):
    """
    GIVEN 1 participant instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 participant and add 0 participant instance into the database and ManualException with code 500
    """
    try:
        _ = participant_service.create(status='pending', member_uuid=pytest.participant_member_uuid,
                                       contest=pytest.contest, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Init
###########
def test_participant_init(reset_db, pause_notification, seed_contest):
    """
    GIVEN 0 participant instance in the database
    WHEN the init method is called
    THEN it should return 1 participant and add 0 participant instance into the database
    """

    participant = participant_service.init(status='pending', member_uuid=pytest.owner_member_uuid)
    assert participant.uuid is not None

    participants = participant_service.find(uuid=participant.uuid)
    assert participants.total == 0
    assert len(participants.items) == 0


def test_participant_init_dup(pause_notification, seed_contest, seed_participant):
    """
    GIVEN 1 participant instance in the database
    WHEN the init method is called with duplicate member_uuid and duplicate party
    THEN it should return 1 participant and init 0 participant instance into the database
    """

    participants = participant_service.find()
    assert participants.total == 1
    assert len(participants.items) == 1

    participant = participant_service.init(status='pending', member_uuid=pytest.owner_member_uuid)
    assert participant.uuid is not None


def test_participant_init_w_bad_member_uuid(reset_db, pause_notification, seed_contest):
    """
    GIVEN 0 participant instance in the database
    WHEN the init method is called with a bad member_uuid
    THEN it should return 1 participant and add 0 participant instance into the database
    """
    participant = participant_service.init(status='pending', contest=pytest.contest, member_uuid=1)
    assert participant.uuid is not None

    # since we have linked the participant instance to an existing contest instance, the find operation will commit
    # it to the db
    try:
        _ = participant_service.find(uuid=participant.uuid)
    except ManualException as ex:
        assert ex.code == 400

    # this is fine because it is not actually being committed to the database
    participant = participant_service.init(status='pending', member_uuid=1)
    assert participant.uuid is not None
    participant_service._rollback()


def test_participant_init_w_bad_field(reset_db, pause_notification, seed_contest):
    """
    GIVEN 0 participant instance in the database
    WHEN the init method is called with a bad field
    THEN it should return 1 participant and add 0 participant instance into the database and ManualException with code 500
    """
    try:
        _ = participant_service.init(status='pending', member_uuid=pytest.owner_member_uuid, contest=pytest.contest,
                                     junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_participant_update(reset_db, pause_notification, seed_contest, seed_owner, seed_participant):
    """
    GIVEN 2 participant instance in the database
    WHEN the update method is called
    THEN it should return 1 participant and update 1 participant instance into the database
    """
    participant = participant_service.update(uuid=pytest.participant.uuid, status='active')
    assert participant.uuid is not None

    participants = participant_service.find(uuid=participant.uuid)
    assert participants.total == 1
    assert len(participants.items) == 1
    assert participants.items[0].status.name == 'active'


def test_participant_update_w_bad_uuid(reset_db, pause_notification, seed_contest, seed_owner):
    """
    GIVEN 1 participant instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 participant and update 0 participant instance into the database and ManualException with code 404
    """
    try:
        _ = participant_service.update(uuid=generate_uuid(), status='completed')
    except ManualException as ex:
        assert ex.code == 404


def test_participant_update_w_bad_field(pause_notification):
    """
    GIVEN 1 participant instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 participant and update 0 participant instance in the database and ManualException with code 400
    """
    try:
        _ = participant_service.update(uuid=pytest.owner.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_participant_apply(reset_db, pause_notification, seed_contest, seed_owner, seed_participant):
    """
    GIVEN 2 participant instance in the database
    WHEN the apply method is called
    THEN it should return 1 participant and update 1 participant instance in the database
    """
    participant = participant_service.apply(instance=pytest.participant, status='active')
    assert participant.uuid is not None

    participants = participant_service.find(uuid=participant.uuid)
    assert participants.total == 1
    assert len(participants.items) == 1


def test_participant_apply_w_bad_field(pause_notification):
    """
    GIVEN 2 participant instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 participant and update 0 participant instance in the database and ManualException with code 400
    """
    try:
        _ = participant_service.apply(instance=pytest.participant, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Misc
###########
def test_create_owner(reset_db, pause_notification, seed_contest):
    """
    GIVEN 0 owner participants in the database
    WHEN the create_owner method is called
    THEN it should return 1 participant and add 1 participant instance into the database
    """
    participant = participant_service.create_owner(member_uuid=pytest.owner_member_uuid, buy_in=pytest.buy_in,
                                                   payout=pytest.payout, contest=pytest.contest)

    assert participant.uuid is not None
    assert participant.member_uuid == pytest.owner_member_uuid


def test_create_owner_bad_member_uuid(reset_db, pause_notification, seed_contest):
    """
    GIVEN 0 owner participants in the database
    WHEN the create_owner method is called with a random member_uuid
    THEN it should return 1 participant and add 1 participant instance into the database
    """
    member_uuid = generate_uuid()
    # this is only working because we are unable to confirm the owner's existence before hand
    participant = participant_service.create_owner(member_uuid=member_uuid, buy_in=pytest.buy_in,
                                                   payout=pytest.payout, contest=pytest.contest)

    assert participant.uuid is not None
    assert participant.member_uuid == member_uuid


def test_create_batch(reset_db, pause_notification, mock_fetch_member, seed_contest, seed_owner):
    """
    GIVEN 1 participants in the database
    WHEN the create_batch method is called with a list of member_uuid's
    THEN it should return nothing but insert the members provided
    """

    participant_service.create_batch(uuids=pytest.participants, contest=pytest.contest)
    participants = participant_service.find()

    assert participants.total == 2


def test_create_batch_bad_members(reset_db, pause_notification, mock_fetch_member, seed_contest, seed_owner):
    """
    GIVEN 1 participants in the database
    WHEN the create_batch method is called with a bad list of member_uuid's
    THEN it should return nothing but insert the members provided with inactive status
    """

    participant_service.create_batch(uuids=[generate_uuid()], contest=pytest.contest)
    participants = participant_service.find()

    assert participants.total == 2

    participants = participant_service.find(status='inactive')
    assert participants.total == 1


def test_create_batch_threaded(reset_db, pause_notification, mock_fetch_member, seed_contest, seed_owner):
    """
    GIVEN 1 participants in the database
    WHEN the create_batch_threaded method is called with a list of member_uuid's
    THEN it should return nothing but insert the members provided using threads
    """

    participant_service.create_batch_threaded(uuids=pytest.participants, contest=pytest.contest)
    participants = participant_service.find()
    assert participants.total == 1
    time.sleep(0.2)
    participants = participant_service.find()
    assert participants.total == 2


def test_create_batch_threaded_bad_members(reset_db, pause_notification, mock_fetch_member, seed_contest, seed_owner):
    """
    GIVEN 1 participants in the database
    WHEN the create_batch_threaded method is called with a bad list of member_uuid's
    THEN it should return nothing but insert the members provided with inactive status using threads
    """

    participant_service.create_batch_threaded(uuids=[generate_uuid()], contest=pytest.contest)
    participants = participant_service.find()
    assert participants.total == 1

    time.sleep(0.1)
    participants = participant_service.find()
    assert participants.total == 2

    participants = participant_service.find(status='inactive')
    assert participants.total == 1


def test__status_machine(reset_db):
    """
    GIVEN 0 pending participant instance
    WHEN the _status_machine method is called
    THEN it should return True when updating status from pending to active and ManualException with code 400 for the inverse
    """
    assert participant_service._status_machine(prev_status='pending', new_status='active')

    try:
        _ = participant_service._status_machine(prev_status='active', new_status='pending')
    except ManualException as ex:
        assert ex.code == 400


def test_fetch_member_user(reset_db, pause_notification, mock_fetch_member_user):
    """
    GIVEN 0 participants in the database
    WHEN the fetch_member_user method is called
    THEN it should return a member from the Member service
    """

    member = participant_service.fetch_member_user(user_uuid=str(pytest.owner_user_uuid),
                                                   league_uuid=str(pytest.league_uuid))
    assert member is not None
    assert member['uuid'] == str(pytest.owner_member_uuid)


def test_fetch_member_user_bad_user_uuid(reset_db, pause_notification, mock_fetch_member_user):
    """
    GIVEN 0 participants in the database
    WHEN the fetch_member_user method is called with a bad user_uuid
    THEN it should return None
    """

    member = participant_service.fetch_member_user(user_uuid=str(generate_uuid()),
                                                   league_uuid=str(pytest.league_uuid))
    assert member is None


def test_fetch_member_user_bad_league_uuid(reset_db, pause_notification, mock_fetch_member_user):
    """
    GIVEN 0 participants in the database
    WHEN the fetch_member_user method is called with a bad league_uuid
    THEN it should return None
    """

    member = participant_service.fetch_member_user(user_uuid=str(pytest.owner_user_uuid),
                                                   league_uuid=str(generate_uuid()))
    assert member is None


def test_fetch_member(reset_db, pause_notification, mock_fetch_member):
    """
    GIVEN 0 participants in the database
    WHEN the fetch_member method is called
    THEN it should return a member from the Member service
    """

    member = participant_service.fetch_member(uuid=str(pytest.owner_member_uuid))
    assert member is not None
    assert member['user_uuid'] == str(pytest.owner_user_uuid)


def test_fetch_member_bad_member_uuid(reset_db, pause_notification, mock_fetch_member):
    """
    GIVEN 0 participants in the database
    WHEN the fetch_member method is called with a bad member_uuid
    THEN it should return None
    """

    member = participant_service.fetch_member(uuid=str(generate_uuid()))
    assert member is None


def test_fetch_member_batch(reset_db, pause_notification, mock_fetch_member_batch):
    """
    GIVEN 0 participants in the database
    WHEN the fetch_member_batch method is called
    THEN it should return a batch of members from the Member service
    """

    batch = participant_service.fetch_member_batch(uuids=[str(pytest.participant_member_uuid)])
    assert batch is not None
    assert len(batch) == 1
    member = batch[0]
    assert member['user_uuid'] == str(pytest.participant_user_uuid)


def test_fetch_member_batch_bad_member_uuid(reset_db, pause_notification, mock_fetch_member_batch):
    """
    GIVEN 0 participants in the database
    WHEN the fetch_member_batch method is called with a bad member_uuid
    THEN it should return empty list
    """

    batch = participant_service.fetch_member_batch(uuids=[str(generate_uuid())])
    assert len(batch) is 0

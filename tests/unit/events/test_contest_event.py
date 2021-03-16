import pytest

from src import services, events
from src.common import time_now

base_service = services.BaseService()


def test_contest_contest_created_sync(reset_db, pause_notification, mock_fetch_location, mock_fetch_member_user,
                                      seed_contest, seed_owner, seed_participant):
    """
    GIVEN 1 contest instance, 1 owner participant instance and 1 participant instance in the database
    WHEN directly calling event contest handle_event contest_created
    THEN it should add 1 contest_materialized instance to the database
    """
    key = 'contest_created'
    value = {
        'uuid': pytest.contest.uuid,
        'league_uuid': pytest.league_uuid,
        'owner_uuid': pytest.owner_user_uuid
    }

    events.Contest().handle_event(key=key, data=value)

    contests = services.ContestMaterializedService().find()

    assert contests.total == 1
    assert contests.items[0].uuid == pytest.contest.uuid


def test_contest_contest_ready_sync(pause_notification):
    """
    GIVEN 1 contest instance, 1 owner participant instance and 1 participant instance in the database
    WHEN directly calling event contest handle_event contest_ready
    THEN it should update 1 contest_materialized instance to the database
    """
    services.ContestService().apply(instance=pytest.contest, status='ready')

    key = 'contest_ready'
    value = {
        'uuid': pytest.contest.uuid,
        'league_uuid': pytest.league_uuid,
        'owner_uuid': pytest.owner_user_uuid
    }

    events.Contest().handle_event(key=key, data=value)

    contests = services.ContestMaterializedService().find()

    assert contests.total == 1
    assert contests.items[0].status == 'ready'


def test_contest_contest_active_sync(pause_notification):
    """
    GIVEN 1 contest instance, 1 owner participant instance and 1 participant instance in the database
    WHEN directly calling event contest handle_event contest_active
    THEN it should update 1 contest_materialized instance to the database
    """
    services.ContestService().apply(instance=pytest.contest, status='active')

    key = 'contest_active'
    value = {
        'uuid': pytest.contest.uuid,
        'league_uuid': pytest.league_uuid,
        'owner_uuid': pytest.owner_user_uuid
    }

    events.Contest().handle_event(key=key, data=value)

    contests = services.ContestMaterializedService().find()

    assert contests.total == 1
    assert contests.items[0].status == 'active'


def test_contest_contest_inactive_sync(pause_notification):
    """
    GIVEN 1 contest instance, 1 owner participant instance and 1 participant instance in the database
    WHEN directly calling event contest handle_event contest_inactive
    THEN it should update 1 contest_materialized instance to the database
    """
    services.ContestService().apply(instance=pytest.contest, status='inactive')

    key = 'contest_inactive'
    value = {
        'uuid': pytest.contest.uuid,
        'league_uuid': pytest.league_uuid,
        'owner_uuid': pytest.owner_user_uuid
    }

    events.Contest().handle_event(key=key, data=value)

    contests = services.ContestMaterializedService().find()

    assert contests.total == 1
    assert contests.items[0].status == 'inactive'


def test_contest_contest_completed_sync(pause_notification):
    """
    GIVEN 1 contest instance, 1 owner participant instance and 1 participant instance in the database
    WHEN directly calling event contest handle_event contest_completed
    THEN it should update 1 contest_materialized instance to the database
    """
    services.ContestService().apply(instance=pytest.contest, status='completed')

    key = 'contest_completed'
    value = {
        'uuid': pytest.contest.uuid,
        'league_uuid': pytest.league_uuid,
        'owner_uuid': pytest.owner_user_uuid
    }

    events.Contest().handle_event(key=key, data=value)

    contests = services.ContestMaterializedService().find()

    assert contests.total == 1
    assert contests.items[0].status == 'completed'


def test_contest_name_updated_sync(pause_notification):
    """
    GIVEN 1 contest instance, 1 owner participant instance and 1 participant instance in the database
    WHEN directly calling event contest handle_event name_updated
    THEN it should update 1 contest_materialized instance to the database
    """
    name = 'Oingo Boingo'
    services.ContestService().apply(instance=pytest.contest, name=name)

    key = 'name_updated'
    value = {
        'uuid': pytest.contest.uuid,
        'league_uuid': pytest.league_uuid,
        'name': name
    }

    events.Contest().handle_event(key=key, data=value)

    contests = services.ContestMaterializedService().find()

    assert contests.total == 1
    assert contests.items[0].name == name


def test_contest_start_time_updated_sync(pause_notification):
    """
    GIVEN 1 contest instance, 1 owner participant instance and 1 participant instance in the database
    WHEN directly calling event contest handle_event start_time_updated
    THEN it should update 1 contest_materialized instance to the database
    """
    start_time = time_now()
    services.ContestService().apply(instance=pytest.contest, start_time=start_time)

    key = 'start_time_updated'
    value = {
        'uuid': pytest.contest.uuid,
        'league_uuid': pytest.league_uuid,
        'start_time': start_time
    }

    events.Contest().handle_event(key=key, data=value)

    contests = services.ContestMaterializedService().find()

    assert contests.total == 1
    assert contests.items[0].start_time == start_time


def test_contest_participant_active_sync(reset_db, pause_notification, mock_fetch_location, mock_fetch_member_user,
                                         mock_fetch_member, seed_contest, seed_owner, seed_participant,
                                         seed_contest_materialized):
    """
    GIVEN 1 contest instance, 1 owner participant instance and 1 participant instance in the database
    WHEN directly calling event contest handle_event participant_active
    THEN it should update 1 contest_materialized instance and update 1 contest instance in the database
    """
    _ = services.ParticipantService().update(uuid=pytest.participant.uuid, status='active')
    key = 'participant_active'
    value = {
        'contest_uuid': str(pytest.contest.uuid),
        'league_uuid': str(pytest.league_uuid),
        'owner_uuid': str(pytest.owner_user_uuid),
        'member_uuid': str(pytest.participant_member_uuid),
        'participant_uuid': str(pytest.participant.uuid),
        'user_uuid': str(pytest.participant_user_uuid),

    }
    events.Contest().handle_event(key=key, data=value)

    contests_materialized = services.ContestMaterializedService().find()
    contests = services.ContestService().find()

    assert contests_materialized.total == 1
    contest_materialized = contests_materialized.items[0]
    assert contest_materialized.uuid == pytest.contest.uuid

    assert contests.total == 1
    contest = contests.items[0]
    assert contest.uuid == pytest.contest.uuid

    assert contest_materialized.participants[str(pytest.participant_member_uuid)] is not None
    assert contest_materialized.participants[str(pytest.owner_member_uuid)] is not None

    assert contest.status.name == 'ready'


def test_contest_participant_inactive_sync(reset_db, pause_notification, mock_fetch_location, mock_fetch_member_user,
                                           mock_fetch_member, seed_contest, seed_owner, seed_participant,
                                           seed_contest_materialized):
    """
    GIVEN 1 contest instance, 1 owner participant instance and 1 participant instance in the database
    WHEN directly calling event contest handle_event participant_inactive
    THEN it should update 1 contest instance in the database
    """
    _ = services.ParticipantService().update(uuid=pytest.participant.uuid, status='inactive')
    key = 'participant_inactive'
    value = {
        'contest_uuid': str(pytest.contest.uuid),
        'league_uuid': str(pytest.league_uuid),
        'owner_uuid': str(pytest.owner_user_uuid),
        'member_uuid': str(pytest.participant_member_uuid),
        'participant_uuid': str(pytest.participant.uuid),
        'user_uuid': str(pytest.participant_user_uuid),

    }
    events.Contest().handle_event(key=key, data=value)

    contests = services.ContestService().find()

    assert contests.total == 1
    contest = contests.items[0]
    assert contest.uuid == pytest.contest.uuid

    assert contest.status.name == 'inactive'


def test_contest_participant_completed_owner_active_participant_completed_sync(reset_db, pause_notification,
                                                                               mock_fetch_location,
                                                                               mock_fetch_member_user,
                                                                               mock_fetch_member, seed_contest,
                                                                               seed_owner, seed_participant,
                                                                               seed_contest_materialized):
    """
    GIVEN 1 contest instance, 1 active owner participant instance and 1 completed participant instance in the database
    WHEN directly calling event contest handle_event participant_completed
    THEN it should update 1 contest_materialized instance
    """
    # update the contest to active from pending
    _ = services.ContestService().update(uuid=pytest.contest.uuid, status='active')

    # update the contest materialized to active from pending and add in a participant
    contest_materialized = services.ContestMaterializedService().update(uuid=pytest.contest.uuid, status='active')
    contest_materialized.participants[str(pytest.participant_member_uuid)] = {
        'member_uuid': str(pytest.participant_member_uuid),
        'display_name': pytest.participant_display_name,
        'status': 'active',
        'score': None,
        'strokes': None
    }
    services.ContestMaterializedService().save(instance=contest_materialized)

    # update the participants to active and completed respectively
    _ = services.ParticipantService().update(uuid=pytest.owner.uuid, status='active')
    _ = services.ParticipantService().update(uuid=pytest.participant.uuid, status='completed')

    key = 'participant_completed'
    value = {
        'contest_uuid': str(pytest.contest.uuid),
        'league_uuid': str(pytest.league_uuid),
        'owner_uuid': str(pytest.owner_user_uuid),
        'member_uuid': str(pytest.participant_member_uuid),
        'participant_uuid': str(pytest.participant.uuid),
        'user_uuid': str(pytest.participant_user_uuid),

    }
    events.Contest().handle_event(key=key, data=value)

    contests_materialized = services.ContestMaterializedService().find()
    contest_materialized = contests_materialized.items[0]

    contests = services.ContestService().find()
    contest = contests.items[0]

    assert contest.status.name == 'active'

    assert contest_materialized.participants[str(pytest.participant_member_uuid)]['status'] == 'completed'


def test_contest_participant_completed_owner_completed_participant_completed_sync(pause_notification,
                                                                                  mock_fetch_location,
                                                                                  mock_fetch_member_user,
                                                                                  mock_fetch_member):
    """
    GIVEN 1 active contest instance, 1 completed owner participant instance and 1 completed participant instance in the database
    WHEN directly calling event contest handle_event participant_completed
    THEN it should update 1 contest_materialized instance and 1 contest instance
    """
    # update the owner participant to completed
    _ = services.ParticipantService().update(uuid=pytest.owner.uuid, status='completed')

    key = 'participant_completed'
    value = {
        'contest_uuid': str(pytest.contest.uuid),
        'league_uuid': str(pytest.league_uuid),
        'owner_uuid': str(pytest.owner_user_uuid),
        'member_uuid': str(pytest.owner_member_uuid),
        'participant_uuid': str(pytest.owner.uuid),
        'user_uuid': str(pytest.owner_user_uuid),

    }
    events.Contest().handle_event(key=key, data=value)

    contests_materialized = services.ContestMaterializedService().find()
    contest_materialized = contests_materialized.items[0]

    contests = services.ContestService().find()
    contest = contests.items[0]

    assert contest.status.name == 'completed'

    assert contest_materialized.participants[str(pytest.owner_member_uuid)]['status'] == 'completed'


def test_contest_avatar_created_sync(pause_notification, mock_upload_fileobj, seed_avatar):
    """
    GIVEN 1 contest instance, 1 owner participant instance and 1 participant instance in the database
    WHEN directly calling event contest handle_event avatar_created
    THEN it should update 1 contest_materialized instance to the database
    """
    key = 'avatar_created'
    value = {
        'contest_uuid': str(pytest.contest.uuid),
        'league_uuid': str(pytest.league_uuid),
        'owner_uuid': str(pytest.owner_user_uuid),
        'uuid': str(pytest.avatar.uuid),
        's3_filename': pytest.avatar.s3_filename
    }

    events.Contest().handle_event(key=key, data=value)

    contests = services.ContestMaterializedService().find()

    assert contests.total == 1
    assert contests.items[0].avatar == pytest.avatar.s3_filename

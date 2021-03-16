import pytest

from src import services


def test_participant_notification_participant_invited(reset_db, kafka_conn_last_msg, mock_contest_notification_create,
                                                      mock_fetch_member, mock_fetch_member_user,
                                                      seed_contest):
    pytest.participant = services.ParticipantService().create(status='pending',
                                                              member_uuid=pytest.participant_member_uuid,
                                                              contest=pytest.contest)
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'participant_invited'
    assert msg.value is not None
    assert msg.value['participant_uuid'] == str(pytest.participant.uuid)


def test_participant_notification_owner_active(kafka_conn_last_msg, mock_fetch_member,
                                               mock_fetch_member_user):
    pytest.owner = services.ParticipantService().create_owner(member_uuid=pytest.owner_member_uuid,
                                                              buy_in=pytest.buy_in, payout=pytest.payout,
                                                              contest=pytest.contest)
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'owner_active'
    assert msg.value is not None
    assert msg.value['participant_uuid'] == str(pytest.owner.uuid)


def test_participant_notification_participant_active(kafka_conn_last_msg, mock_fetch_member):
    _ = services.ParticipantService().update(uuid=pytest.participant.uuid, status='active')
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'participant_active'
    assert msg.value is not None
    assert msg.value['participant_uuid'] == str(pytest.participant.uuid)


def test_participant_notification_participant_completed(kafka_conn_last_msg, mock_fetch_member):
    _ = services.ParticipantService().update(uuid=pytest.participant.uuid, status='completed')
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'participant_completed'
    assert msg.value is not None
    assert msg.value['participant_uuid'] == str(pytest.participant.uuid)


def test_participant_notification_participant_inactive(kafka_conn_last_msg, mock_fetch_member):
    _ = services.ParticipantService().update(uuid=pytest.participant.uuid, status='inactive')
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'participant_inactive'
    assert msg.value is not None
    assert msg.value['participant_uuid'] == str(pytest.participant.uuid)

import pytest

from src import services
from src.common import time_now


def test_contest_notification_contest_created(reset_db, kafka_conn_last_msg):
    pytest.contest = services.ContestService().create(status='pending', owner_uuid=pytest.owner_user_uuid,
                                                      name=pytest.name,
                                                      start_time=pytest.start_time, location_uuid=pytest.location_uuid,
                                                      league_uuid=pytest.league_uuid)
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'contest_created'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.contest.uuid)


def test_contest_notification_contest_ready(kafka_conn_last_msg):
    pytest.contest = services.ContestService().update(uuid=pytest.contest.uuid, status='ready')
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'contest_ready'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.contest.uuid)


def test_contest_notification_contest_active(kafka_conn_last_msg):
    pytest.contest = services.ContestService().update(uuid=pytest.contest.uuid, status='active')
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'contest_active'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.contest.uuid)


def test_contest_notification_contest_completed(kafka_conn_last_msg):
    pytest.contest = services.ContestService().update(uuid=pytest.contest.uuid, status='completed')
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'contest_completed'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.contest.uuid)


def test_contest_notification_contest_inactive(kafka_conn_last_msg):
    pytest.contest = services.ContestService().update(uuid=pytest.contest.uuid, status='inactive')
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'contest_inactive'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.contest.uuid)


def test_contest_notification_avatar_created(kafka_conn_last_msg, seed_avatar):
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'avatar_created'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.avatar.uuid)


def test_contest_notification_name_updated(kafka_conn_last_msg):
    name = 'Oingo Boingo'
    pytest.contest = services.ContestService().update(uuid=pytest.contest.uuid, name=name)
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'name_updated'
    assert msg.value is not None
    assert msg.value['name'] == name


def test_contest_notification_start_time(kafka_conn_last_msg):
    start_time = time_now()
    pytest.contest = services.ContestService().update(uuid=pytest.contest.uuid, start_time=start_time)
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'start_time_updated'
    assert msg.value is not None
    assert msg.value['start_time'] == start_time

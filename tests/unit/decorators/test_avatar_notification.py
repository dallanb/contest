import time

import pytest

from src import services


def test_avatar_notification_avatar_created(reset_db, kafka_conn_last_msg, seed_contest, seed_avatar):
    time.sleep(0.5)
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'avatar_created'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.avatar.uuid)


def test_avatar_notification_avatar_updated(kafka_conn_last_msg):
    s3_filename = services.AvatarService().generate_s3_filename(contest_uuid=str(pytest.contest.uuid))
    services.AvatarService().apply(instance=pytest.avatar, s3_filename=s3_filename)
    time.sleep(0.2)
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'avatar_updated'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.avatar.uuid)


def test_avatar_notification_avatar_deleted(kafka_conn_last_msg):
    services.AvatarService().destroy(instance=pytest.avatar)
    time.sleep(0.2)
    msg = kafka_conn_last_msg('contests')
    assert msg.key is not None
    assert msg.key == 'avatar_deleted'
    assert msg.value is not None
    assert msg.value['uuid'] == str(pytest.avatar.uuid)
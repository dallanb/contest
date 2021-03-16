import json

import pytest

from src import app, services


###########
# Create
###########
def test_create_avatar(reset_db, mock_fetch_member, mock_fetch_member_user, mock_upload_fileobj,
                       pause_notification, seed_contest):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'avatar' is requested
    THEN check that the response is valid
    """
    contest_uuid = pytest.contest.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.owner_user_uuid}

    # Payload
    payload = {'avatar': ''}

    # Request
    response = app.test_client().post(f'/contests/{contest_uuid}/avatars', data=payload,
                                      headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    avatars = response['data']['avatars']
    assert avatars['uuid'] is not None
    assert avatars['s3_filename'] == f"{str(contest_uuid)}.jpeg"


def test_update_avatar(mock_upload_fileobj):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'avatar' is requested
    THEN check that the response is valid
    """
    contest = services.ContestService().find().items[0]
    contest_uuid = contest.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.owner_user_uuid}

    # Payload
    payload = {'avatar': ''}

    # Request
    response = app.test_client().post(f'/contests/{contest_uuid}/avatars', data=payload,
                                      headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    avatars = response['data']['avatars']
    assert avatars['uuid'] is not None
    assert avatars['s3_filename'] == f"{str(contest_uuid)}.jpeg"

    # ensure that we still only have one avatar instance in the database
    avatar = services.AvatarService().find()
    assert avatar.total == 1

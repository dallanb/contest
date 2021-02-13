import json

import pytest

from src import app


###########
# Create
###########
def test_create_participant(reset_db, mock_fetch_member, mock_fetch_member_user, seed_contest):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'participants' is requested
    THEN check that the response is valid
    """
    contest_uuid = pytest.contest.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.owner_user_uuid}

    # Payload
    payload = {'member_uuid': pytest.participant_member_uuid}

    # Request
    response = app.test_client().post(f'/contests/{contest_uuid}/participants', json=payload,
                                      headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    participants = response['data']['participants']
    assert participants['status'] == 'pending'
    assert participants['uuid'] is not None
    assert participants['member_uuid'] == str(pytest.participant_member_uuid)


###########
# Fetch
###########
def test_fetch_participant(reset_db, seed_contest, seed_participant):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'contest' is requested
    THEN check that the response is valid
    """
    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.owner_user_uuid}

    # Request
    response = app.test_client().get(f'/participants/{pytest.participant.uuid}',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    participants = response['data']['participants']
    assert participants['uuid'] == str(pytest.participant.uuid)
    assert participants['member_uuid'] == str(pytest.participant_member_uuid)
    assert participants['status'] == 'pending'


def test_fetch_participant_member(reset_db, seed_contest, seed_participant):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participant_member' is requested
    THEN check that the response is valid
    """
    contest_uuid = pytest.contest.uuid
    member_uuid = pytest.participant_member_uuid
    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.owner_user_uuid}

    # Request
    response = app.test_client().get(
        f'/contests/{contest_uuid}/participants/member/{member_uuid}',
        headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    participants = response['data']['participants']
    assert participants['uuid'] == str(pytest.participant.uuid)
    assert participants['member_uuid'] == str(member_uuid)
    assert participants['status'] == 'pending'


###########
# Fetch All
###########
def test_fetch_all_participant(reset_db, seed_contest, seed_participant):
    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.owner_user_uuid}

    # Request
    response = app.test_client().get('/participants',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"

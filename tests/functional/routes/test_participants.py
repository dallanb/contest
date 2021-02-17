import json

import pytest

from src import app, services


###########
# Create
###########
def test_create_participant(reset_db, mock_fetch_member, mock_fetch_member_user, pause_notification, seed_contest):
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
def test_fetch_participant(reset_db, pause_notification, seed_contest, seed_participant):
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


def test_fetch_participant_member(reset_db, pause_notification, seed_contest, seed_participant):
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
def test_fetch_all_participant(reset_db, pause_notification, seed_contest, seed_participant):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participants' is requested
    THEN check that the response is valid
    """
    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.owner_user_uuid}

    # Request
    response = app.test_client().get('/participants',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"


###########
# Update
###########
def test_update_participant(mock_fetch_member, pause_notification):
    """
    GIVEN a Flask application configured for testing
    WHEN the PUT endpoint 'participant' is requested
    THEN check that the response is valid
    """
    participant = services.ParticipantService().find().items[0]
    participant_uuid = participant.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.owner_user_uuid}

    # Payload
    payload = {'status': 'active'}

    # Request
    response = app.test_client().put(f'/participants/{participant_uuid}', json=payload, headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    participants = response['data']['participants']
    assert participants['uuid'] == str(participant_uuid)
    assert participants['status'] == 'active'

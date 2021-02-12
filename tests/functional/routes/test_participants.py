import json

from src import app
from tests.helpers import generate_uuid


###########
# Create
###########
def test_create_participant(get_user_uuid, get_sport_uuid, get_participant_uuid, create_contest):
    user_uuid = get_user_uuid()
    sport_uuid = get_sport_uuid()
    contest = create_contest(owner_uuid=user_uuid, sport_uuid=sport_uuid)
    contest_uuid = contest.uuid

    participant_user_uuid = generate_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Payload
    payload = {'user_uuid': participant_user_uuid}

    # Request
    response = app.test_client().post(f'contests/{contest_uuid}/participants', json=payload,
                                      headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['participants']['status'] == 'pending'
    assert response['data']['participants']['uuid'] is not None


###########
# Fetch
###########
def test_fetch_participant(get_user_uuid, get_sport_uuid, get_participant_uuid, create_contest, create_participant):
    user_uuid = get_user_uuid()
    sport_uuid = get_sport_uuid()
    contest = create_contest(owner_uuid=user_uuid, sport_uuid=sport_uuid)
    contest_uuid = contest.uuid
    participant = create_participant(contest_uuid=contest_uuid, user_uuid=user_uuid)
    participant_uuid = participant.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get(f'/participants/{participant_uuid}',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['participants']['uuid'] == str(participant_uuid)


###########
# Fetch All
###########
def test_fetch_all_participant(get_user_uuid):
    user_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/participants',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"

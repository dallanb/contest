import json
from datetime import datetime

import pytest

from src import app, services


#############
# SUCCESS
#############

###########
# Create
###########
def test_create_contest(reset_db, mock_fetch_member_user, mock_fetch_member, mock_fetch_member_batch,
                        mock_fetch_location):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'contests' is requested
    THEN check that the response is valid
    """

    # Header
    headers = {'X-Consumer-Custom-ID': pytest.owner_user_uuid}

    # Payload
    payload = {
        'sport_uuid': pytest.sport_uuid,
        'location_uuid': pytest.location_uuid,
        'league_uuid': pytest.league_uuid,
        'name': pytest.name,
        'start_time': pytest.start_time,
        'participants': pytest.participants,
        'buy_in': pytest.buy_in,
        'payout': pytest.payout
    }

    # Request
    response = app.test_client().post('/contests', headers=headers, json=payload)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    contests = response['data']['contests']
    assert contests['status'] == 'pending'
    assert contests['uuid'] is not None
    assert contests['owner_uuid'] == str(pytest.owner_user_uuid)
    assert contests['name'] == pytest.name
    assert contests['start_time'] == pytest.start_time
    assert contests['league_uuid'] == str(pytest.league_uuid)
    assert contests['location_uuid'] == str(pytest.location_uuid)

    # confirm sport creation
    sports = services.SportService().find()
    assert sports.total == 1

    sport = sports.items[0]
    assert sport.sport_uuid == pytest.sport_uuid
    assert str(sport.contest_uuid) == contests['uuid']

    # confirm owner creation
    participants = services.ParticipantService().find(member_uuid=pytest.owner_member_uuid)
    assert participants.total == 1

    owner = participants.items[0]
    assert str(owner.contest_uuid) == contests['uuid']
    assert owner.status.name == 'active'

    # confirm participant creation
    participants = services.ParticipantService().find(member_uuid=pytest.participant_member_uuid)
    assert participants.total == 1

    participant = participants.items[0]
    assert str(participant.contest_uuid) == contests['uuid']
    assert participant.status.name == 'pending'

    # confirm contest_materialized creation
    contests_materialized = services.ContestMaterializedService().find()
    assert contests_materialized.total == 1

    contest_materialized = contests_materialized.items[0]
    assert str(contest_materialized.uuid) == contests['uuid']
    assert str(contest_materialized.location) == pytest.course_name

    materialized_participants = contest_materialized.participants
    assert materialized_participants[str(owner.member_uuid)] is not None


###########
# Fetch
###########
def test_fetch_contest(reset_db, seed_contest):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'contest' is requested
    THEN check that the response is valid
    """
    contest_uuid = pytest.contest.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.owner_user_uuid}

    # Request
    response = app.test_client().get(f'/contests/{contest_uuid}',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    contests = response['data']['contests']
    assert contests['status'] == 'pending'
    assert contests['uuid'] == str(contest_uuid)
    assert contests['owner_uuid'] == str(pytest.owner_user_uuid)
    assert contests['name'] == pytest.name
    assert contests['start_time'] == pytest.start_time
    assert contests['league_uuid'] == str(pytest.league_uuid)
    assert contests['location_uuid'] == str(pytest.location_uuid)


def test_fetch_contest_materialized(reset_db, seed_contest, seed_contest_materialized):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'contest_materialized' is requested
    THEN check that the response is valid
    """
    contest_uuid = pytest.contest_materialized.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.owner_user_uuid}

    # Request
    response = app.test_client().get(f'/contests/materialized/{contest_uuid}',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    contests = response['data']['contests']
    assert contests['status'] == 'pending'
    assert contests['uuid'] == str(contest_uuid)
    assert contests['owner'] == str(pytest.owner_user_uuid)
    assert contests['name'] == pytest.name
    assert contests['start_time'] == pytest.start_time
    assert contests['league'] == str(pytest.league_uuid)
    assert contests['location'] == str(pytest.course_name)
    assert len(contests['participants']) == 1


###########
# Fetch All
###########
def test_fetch_all_contest(reset_db, seed_contest):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'contests' is requested
    THEN check that the response is valid
    """
    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.owner_user_uuid}

    # Request
    response = app.test_client().get('/contests',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['contests']) == 1
    contests = response['data']['contests'][0]
    assert contests['status'] == 'pending'
    assert contests['uuid'] == str(pytest.contest.uuid)
    assert contests['owner_uuid'] == str(pytest.owner_user_uuid)
    assert contests['name'] == pytest.name
    assert contests['start_time'] == pytest.start_time
    assert contests['league_uuid'] == str(pytest.league_uuid)
    assert contests['location_uuid'] == str(pytest.location_uuid)


def test_fetch_all_contest_materialized(reset_db, seed_contest, seed_contest_materialized):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'contests_materialized' is requested
    THEN check that the response is valid
    """
    contest_uuid = pytest.contest_materialized.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.owner_user_uuid}

    # Request
    response = app.test_client().get(f'/contests/materialized',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['contests']) == 1
    contests = response['data']['contests'][0]
    assert contests['status'] == 'pending'
    assert contests['uuid'] == str(contest_uuid)
    assert contests['owner'] == str(pytest.owner_user_uuid)
    assert contests['name'] == pytest.name
    assert contests['start_time'] == pytest.start_time
    assert contests['league'] == str(pytest.league_uuid)
    assert contests['location'] == str(pytest.course_name)
    assert len(contests['participants']) == 1


def test_fetch_all_contest_calendar(reset_db, seed_contest):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'contests_calender' is requested
    THEN check that the response is valid
    """
    month = datetime.now().month
    year = datetime.now().year

    # Headers
    headers = {'X-Consumer-Custom-ID': pytest.owner_user_uuid}

    # Params
    params = {'league_uuid': pytest.league_uuid, 'month': month, 'year': year}

    # Request
    response = app.test_client().get('/contests/calendar',
                                     headers=headers, query_string=params)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert len(response['data']['contests']) == 1
    contests = response['data']['contests'][0]
    assert contests['status'] == 'pending'
    assert contests['uuid'] == str(pytest.contest.uuid)
    assert contests['owner_uuid'] == str(pytest.owner_user_uuid)
    assert contests['name'] == pytest.name
    assert contests['start_time'] == pytest.start_time
    assert contests['league_uuid'] == str(pytest.league_uuid)
    assert contests['location_uuid'] == str(pytest.location_uuid)


#############
# FAIL
#############

###########
# Create
###########
def test_create_contest_fail(reset_db, mock_fetch_member_user, mock_fetch_member, mock_fetch_member_batch,
                             mock_fetch_location):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'contests' is requested with incorrect data
    THEN check that the response is valid
    """
    # Header
    headers = {'X-Consumer-Custom-ID': pytest.owner_user_uuid}

    # Payload
    payload = {
        'sport_uuid': pytest.sport_uuid,
        'location_uuid': pytest.location_uuid,
        'league_uuid': pytest.league_uuid,
        'name': None,
        'start_time': pytest.start_time,
        'participants': pytest.participants,
        'buy_in': pytest.buy_in,
        'payout': pytest.payout
    }

    # Request
    response = app.test_client().post('/contests', headers=headers, json=payload)

    # Response
    assert response.status_code == 400

import json

from src import app


#############
# SUCCESS
#############

###########
# Create
###########


def test_create_contest(mocker, reset_db, get_user_uuid, get_sport_uuid, get_location_uuid, get_league_uuid, get_name,
                        get_start_time,
                        get_participants, get_buy_in,
                        get_payout, mock_fetch_member_user, mock_fetch_member, mock_fetch_member_batch,
                        mock_fetch_location):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'contests' is requested
    THEN check that the response is valid
    """

    sport_uuid = get_sport_uuid()
    location_uuid = get_location_uuid()
    league_uuid = get_league_uuid()
    name = get_name()
    start_time = get_start_time()
    participants = get_participants()
    buy_in = get_buy_in()
    payout = get_payout()

    mocker.patch('src.services.ParticipantService.fetch_member_user', mock_fetch_member_user)
    mocker.patch('src.services.ParticipantService.fetch_member', mock_fetch_member)
    mocker.patch('src.services.ParticipantService.fetch_member_batch', mock_fetch_member_batch)
    mocker.patch('src.services.ContestService.fetch_location', mock_fetch_location)

    user_uuid = get_user_uuid()
    # Header
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Payload
    payload = {
        'sport_uuid': sport_uuid,
        'location_uuid': location_uuid,
        'league_uuid': league_uuid,
        'name': name,
        'start_time': start_time,
        'participants': participants,
        'buy_in': buy_in,
        'payout': payout
    }

    # Request
    response = app.test_client().post('/contests', headers=headers, json=payload)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['contests']['status'] == 'pending'
    assert response['data']['contests']['uuid'] is not None


###########
# Fetch
###########
def test_fetch_contest(get_user_uuid, get_sport_uuid, create_contest):
    user_uuid = get_user_uuid()
    sport_uuid = get_sport_uuid()

    contest = create_contest(owner_uuid=user_uuid, sport_uuid=sport_uuid)
    contest_uuid = contest.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get(f'/contests/{contest_uuid}',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['contests']['uuid'] == str(contest_uuid)


###########
# Fetch All
###########
def test_fetch_all_contest(get_user_uuid):
    user_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/contests',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"

import json
from src import app


###########
# Create
###########
def test_create_contest(get_user_uuid, get_contest_uuid):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Payload
    payload = {'contest_uuid': contest_uuid}

    # Request
    response = app.test_client().post('/contests', json=payload,
                                      headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['contests']['status'] == 'pending'
    assert response['data']['contests']['uuid'] is not None


###########
# Fetch
###########
def test_fetch_contest(get_user_uuid, get_contest_uuid, create_contest):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()

    contest = create_contest(owner_uuid=user_uuid, contest_uuid=contest_uuid)
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


def test_fetch_all_contest_include_parties(get_user_uuid):
    user_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/contests?include=parties',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data'] is not None
    assert response['data']['contests'] is not None
    assert response['data']['contests'][0]['parties'] is not None


def test_fetch_all_contest_include_participants(get_user_uuid):
    user_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/contests?include=parties.participants',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data'] is not None
    assert response['data']['contests'] is not None
    assert response['data']['contests'][0]['parties'] is not None
    assert response['data']['contests'][0]['parties'][0]['participants'] is not None

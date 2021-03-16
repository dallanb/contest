import pytest

from src import services
from src.common import ParticipantStatusEnum
from tests.helpers import fetch_member_user, fetch_location


@pytest.fixture(scope="function")
def seed_contest_materialized():
    owner = fetch_member_user(None, user_uuid=str(pytest.owner_user_uuid), league_uuid=str(pytest.league_uuid))
    location = fetch_location(None, uuid=str(pytest.location_uuid))

    pytest.contest_materialized = services.ContestMaterializedService().create(
        uuid=pytest.contest.uuid, name=pytest.name, status=pytest.contest.status.name,
        start_time=pytest.start_time,
        owner=pytest.owner_user_uuid, location=location.get('name', ''), league=pytest.league_uuid,
        participants={str(owner.get('uuid', '')): {
            'member_uuid': str(owner.get('uuid', '')),
            'display_name': owner.get('display_name', ''),
            'status': ParticipantStatusEnum['active'].name,
            'score': None,
            'strokes': None,
        }})

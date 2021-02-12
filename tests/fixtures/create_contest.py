import pytest
from src import services


@pytest.fixture
def create_contest():
    def _method(owner_uuid, sport_uuid):
        contest = services.ContestService().create(owner_uuid=owner_uuid, status='pending')
        _ = services.SportService().create(sport_uuid=sport_uuid, contest=contest)
        return contest

    return _method

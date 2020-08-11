import pytest
from src import services


@pytest.fixture
def create_contest():
    def _method(owner_uuid, sport_uuid):
        contest = services.init_contest(owner_uuid=owner_uuid, status='pending')

        # contest (possibly handle this asynchronously)
        _ = services.init_sport(sport_uuid=sport_uuid, contest=contest)

        contest = services.save_contest(contest)
        return contest

    return _method

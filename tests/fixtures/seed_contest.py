import pytest

from src import services


@pytest.fixture(scope="function")
def seed_contest(mock_contest_notification_create):
    pytest.contest = services.ContestService().create(status='pending', owner_uuid=pytest.owner_user_uuid,
                                                      name=pytest.name,
                                                      start_time=pytest.start_time, location_uuid=pytest.location_uuid,
                                                      league_uuid=pytest.league_uuid)

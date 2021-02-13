import pytest

from src import services


@pytest.fixture(scope="function")
def seed_sport():
    pytest.sport = services.SportService().create(sport_uuid=pytest.sport_uuid, contest=pytest.contest)

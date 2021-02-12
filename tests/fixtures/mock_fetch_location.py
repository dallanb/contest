import pytest

from tests.helpers import fetch_location


@pytest.fixture
def mock_fetch_location(mocker):
    yield mocker.patch('src.services.ContestService.fetch_location', fetch_location)

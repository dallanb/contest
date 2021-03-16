import pytest

from tests.helpers import fetch_member_user


@pytest.fixture
def mock_fetch_member_user(mocker):
    yield mocker.patch('src.services.ParticipantService.fetch_member_user', fetch_member_user)

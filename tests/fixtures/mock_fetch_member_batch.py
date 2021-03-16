import pytest

from tests.helpers import fetch_member_batch


@pytest.fixture
def mock_fetch_member_batch(mocker):
    yield mocker.patch('src.services.ParticipantService.fetch_member_batch', fetch_member_batch)

import pytest

from src import services


@pytest.fixture
def mock_create_batch_async(mocker):
    yield mocker.patch('src.services.ParticipantService.create_batch_async', services.ParticipantService().create_batch)

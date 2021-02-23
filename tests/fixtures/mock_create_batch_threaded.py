import pytest

from src import services


@pytest.fixture
def mock_create_batch_threaded(mocker):
    yield mocker.patch('src.services.ParticipantService.create_batch_threaded', services.ParticipantService().create_batch)

import pytest
from src import services


@pytest.fixture
def create_participant():
    def _method(contest_uuid, user_uuid):
        return services.Participant().create(contest_uuid=contest_uuid, user_uuid=user_uuid, status='pending')

    return _method

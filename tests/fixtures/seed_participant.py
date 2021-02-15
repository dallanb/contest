import pytest

from src import services


@pytest.fixture(scope="function")
def seed_participant(mock_participant_notification_create):
    pytest.participant = services.ParticipantService().create(status='pending',
                                                              member_uuid=pytest.participant_member_uuid,
                                                              contest=pytest.contest)

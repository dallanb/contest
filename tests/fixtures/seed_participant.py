import pytest

from src import services


@pytest.fixture(scope="function")
def seed_participant():
    pytest.participant = services.ParticipantService().create(status='pending',
                                                              member_uuid=pytest.participant_member_uuid,
                                                              contest=pytest.contest)

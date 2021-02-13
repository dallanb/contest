import pytest

from src import services


@pytest.fixture(scope="function")
def seed_participant():
    instance = services.ParticipantService().init(status='pending', member_uuid=pytest.participant_member_uuid,
                                                  contest=pytest.contest)
    pytest.participant = services.ParticipantService().save(instance=instance)

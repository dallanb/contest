import pytest

from src import services


@pytest.fixture(scope="function")
def seed_owner():
    pytest.owner = services.ParticipantService().create_owner(member_uuid=pytest.owner_member_uuid,
                                                              contest=pytest.contest,
                                                              buy_in=pytest.buy_in,
                                                              payout=pytest.payout)

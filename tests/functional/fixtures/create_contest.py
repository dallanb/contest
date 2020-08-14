import pytest
from src import services, model


@pytest.fixture
def create_contest():
    def _method(owner_uuid, sport_uuid):
        base = services.Base()
        contest = base.init(model=model.Contest, owner_uuid=owner_uuid, status='pending')

        # contest (possibly handle this asynchronously)
        _ = base.init(model=model.Sport, sport_uuid=sport_uuid, contest=contest)

        contest = base.save(instance=contest)
        return contest

    return _method

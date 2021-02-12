from uuid import uuid4

import pytest

global_league_uuid = uuid4()


@pytest.fixture
def get_league_uuid():
    def _method():
        return global_league_uuid

    return _method

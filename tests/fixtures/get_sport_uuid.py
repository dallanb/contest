import pytest
from uuid import uuid4

global_sport_uuid = uuid4()


@pytest.fixture
def get_sport_uuid():
    def _method():
        return global_sport_uuid

    return _method

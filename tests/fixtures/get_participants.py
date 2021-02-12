from uuid import uuid4

import pytest

global_participants = [uuid4(), uuid4()]


@pytest.fixture
def get_participants():
    def _method():
        return global_participants

    return _method

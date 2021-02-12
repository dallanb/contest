from uuid import uuid4

import pytest

global_location_uuid = uuid4()


@pytest.fixture
def get_location_uuid():
    def _method():
        return global_location_uuid

    return _method

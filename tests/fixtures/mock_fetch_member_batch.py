import pytest

from tests.helpers import generate_uuid


@pytest.fixture
def mock_fetch_member_batch():
    def _method(self, **kwargs):
        uuids = kwargs.get('uuids')
        return []

    return _method

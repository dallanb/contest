import pytest

from tests.helpers import generate_uuid


@pytest.fixture
def mock_fetch_member():
    def _method(self, **kwargs):
        member = kwargs.get('uuid')
        return {'user_uuid': generate_uuid()}

    return _method

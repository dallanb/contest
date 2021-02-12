import pytest

from tests.helpers import generate_uuid


@pytest.fixture
def mock_fetch_location():
    def _method(self, **kwargs):
        course = kwargs.get('uuid')
        return {'name': 'Test Course'}

    return _method

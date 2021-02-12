import pytest

from tests.helpers import generate_uuid


@pytest.fixture
def mock_fetch_member_user():
    def _method(self, **kwargs):
        user = kwargs.get('user_uuid')
        league = kwargs.get('league_uuid')
        return {'display_name': 'Dallan Bhatti', 'uuid': generate_uuid()}

    return _method

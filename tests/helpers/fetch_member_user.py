import pytest


def fetch_member_user(self, user_uuid, league_uuid):
    if user_uuid == str(pytest.owner_user_uuid) and league_uuid == str(pytest.league_uuid):
        return {
            'user_uuid': user_uuid,
            'league_uuid': league_uuid,
            'display_name': pytest.owner_display_name,
            'uuid': str(pytest.owner_member_uuid)
        }
    else:
        return 500

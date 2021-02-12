import pytest


def fetch_member(self, uuid):
    if uuid == str(pytest.owner_member_uuid):
        return {
            'uuid': str(pytest.owner_member_uuid),
            'user_uuid': str(pytest.owner_user_uuid),
            'display_name': pytest.owner_display_name
        }
    elif uuid == str(pytest.participant_member_uuid):
        return {
            'uuid': str(pytest.participant_member_uuid),
            'user_uuid': str(pytest.owner_user_uuid),
            'display_name': pytest.owner_display_name
        }
    else:
        return 500

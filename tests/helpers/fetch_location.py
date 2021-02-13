import pytest


def fetch_location(self, uuid):
    if uuid == str(pytest.location_uuid):
        return {'name': pytest.course_name}
    else:
        return None

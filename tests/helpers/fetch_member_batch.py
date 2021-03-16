import pytest

from tests.helpers import fetch_member


def fetch_member_batch(self, uuids):
    member_batch = []
    if str(pytest.participant_member_uuid) in uuids:
        participant = fetch_member(None, uuid=str(pytest.participant_member_uuid))
        member_batch.append(participant)
    return member_batch

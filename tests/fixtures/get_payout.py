import pytest

global_payout = [0.75, 0.25]


@pytest.fixture
def get_payout():
    def _method():
        return global_payout

    return _method

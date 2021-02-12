import pytest

global_buy_in = 5.0


@pytest.fixture
def get_buy_in():
    def _method():
        return global_buy_in

    return _method

import pytest

global_name = 'Super Contest'


@pytest.fixture
def get_name():
    def _method():
        return global_name

    return _method

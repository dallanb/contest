import pytest

from src.common import time_now

global_start_time = time_now()


@pytest.fixture
def get_start_time():
    def _method():
        return global_start_time

    return _method

from uuid import uuid4

import pytest

from src.common import time_now
from .fixtures import *


def pytest_configure(config):
    pytest.contest = None
    pytest.contest_materialized = None
    pytest.sport = None
    pytest.buy_in = 5.0
    pytest.location_uuid = uuid4()
    pytest.league_uuid = uuid4()
    pytest.name = 'Super Contest'
    pytest.owner_user_uuid = uuid4()
    pytest.owner_member_uuid = uuid4()
    pytest.owner_display_name = 'Dallan Bhatti'
    pytest.participant_user_uuid = uuid4()
    pytest.participant_member_uuid = uuid4()
    pytest.participant_display_name = 'LeBron James'
    pytest.participants = [pytest.owner_member_uuid, pytest.participant_member_uuid]
    pytest.payout = [0.75, 0.25]
    pytest.sport_uuid = uuid4()
    pytest.start_time = time_now()
    pytest.course_name = 'Super Course'

import time

import pytest

from src import events, services
from tests.helpers import generate_uuid


def test_score_stroke_update_sync(reset_db, pause_notification, mock_fetch_location, mock_fetch_member_user,
                                  seed_contest, seed_owner, seed_participant, seed_contest_materialized):
    """
    GIVEN 1 contest instance, 1 contest_materialized instance, 1 owner participant instance and 1 participant instance in the database
    WHEN directly calling event contest handle_event contest_created
    THEN it should add 1 contest_materialized instance to the database
    """
    key = 'stroke_update'
    value = {
        'uuid': str(generate_uuid()),
        'contest_uuid': str(pytest.contest.uuid),
        'sheet_uuid': str(generate_uuid()),
        'participant_uuid': str(pytest.owner_member_uuid),
        'strokes': 3,
        'score': -1,
    }

    events.Score().handle_event(key=key, data=value)

    contests = services.ContestMaterializedService().find()

    assert contests.total == 1
    assert contests.items[0].uuid == pytest.contest.uuid
    contest = contests.items[0]
    assert contest.participants[str(pytest.owner_member_uuid)]['strokes'] == 3
    assert contest.participants[str(pytest.owner_member_uuid)]['score'] == -1

# def test_score_stroke_update_async(reset_db, pause_notification, kafka_conn_custom_topics, seed_contest, seed_owner,
#                                    seed_participant, seed_contest_materialized):
#     """
#     GIVEN 1 contest instance, 1 contest_materialized instance, 1 owner participant instance and 1 participant instance in the database
#     WHEN the SCORE service notifies Kafka that a scorecard has been updated
#     THEN event score handle_event stoke_update updates 1 contest_materialized instance in the database
#     """
#     kafka_conn_custom_topics(['scores_test'])
#     time.sleep(1)
#
#     key = 'stroke_update'
#     value = {
#         'uuid': str(generate_uuid()),
#         'contest_uuid': str(pytest.contest.uuid),
#         'sheet_uuid': str(generate_uuid()),
#         'participant_uuid': str(pytest.owner_member_uuid),
#         'strokes': 3,
#         'score': -1,
#     }
#
#     services.BaseService().notify(topic='scores_test', value=value, key=key)
#     time.sleep(1)
#
#     contests = services.ContestMaterializedService().find()
#
#     assert contests.total == 1
#     assert contests.items[0].uuid == pytest.contest.uuid
#     contest = contests.items[0]
#     assert contest.participants[str(pytest.owner_member_uuid)]['strokes'] == 3
#     assert contest.participants[str(pytest.owner_member_uuid)]['score'] == -1

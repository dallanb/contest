import pytest


@pytest.fixture(scope="function")
def pause_notification(mock_contest_notification_create, mock_contest_notification_update,
                       mock_participant_notification_create, mock_participant_notification_create_owner,
                       mock_participant_notification_update):
    return True

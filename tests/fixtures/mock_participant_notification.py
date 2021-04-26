import pytest

from tests.helpers import participant_notification_create, participant_notification_create_owner, \
    participant_notification_update


@pytest.fixture
def mock_participant_notification_create(mocker):
    yield mocker.patch('src.decorators.notifications.participant_notification.create', participant_notification_create)


@pytest.fixture
def mock_participant_notification_create_owner(mocker):
    yield mocker.patch('src.decorators.notifications.participant_notification.create_owner', participant_notification_create_owner)


@pytest.fixture
def mock_participant_notification_update(mocker):
    yield mocker.patch('src.decorators.notifications.participant_notification.update', participant_notification_update)

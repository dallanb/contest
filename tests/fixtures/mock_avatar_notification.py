import pytest

from tests.helpers import avatar_notification_create, avatar_notification_delete, avatar_notification_update


@pytest.fixture
def mock_avatar_notification_create(mocker):
    yield mocker.patch('src.decorators.notifications.avatar_notification.create', avatar_notification_create)


@pytest.fixture
def mock_avatar_notification_delete(mocker):
    yield mocker.patch('src.decorators.notifications.avatar_notification.delete', avatar_notification_delete)


@pytest.fixture
def mock_avatar_notification_update(mocker):
    yield mocker.patch('src.decorators.notifications.avatar_notification.update', avatar_notification_update)

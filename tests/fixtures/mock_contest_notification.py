import pytest

from tests.helpers import contest_notification, contest_notification_create, contest_notification_update


@pytest.fixture
def mock_contest_notification(mocker):
    yield mocker.patch('src.decorators.contest_notification', contest_notification)


@pytest.fixture
def mock_contest_notification_create(mocker):
    yield mocker.patch('src.decorators.contest_notification.create', contest_notification_create)


@pytest.fixture
def mock_contest_notification_update(mocker):
    yield mocker.patch('src.decorators.contest_notification.update', contest_notification_update)

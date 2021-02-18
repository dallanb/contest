import pytest

from src import services


@pytest.fixture(scope="function")
def seed_avatar():
    s3_filename = services.AvatarService().generate_s3_filename(contest_uuid=str(pytest.contest.uuid))
    pytest.avatar = services.AvatarService().create(s3_filename=s3_filename)
    services.ContestService().apply(instance=pytest.contest, avatar=pytest.avatar)

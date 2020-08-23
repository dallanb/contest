import logging
from http import HTTPStatus
from .base import Base
from ..models import Contest as ContestModel


class Contest(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.contest_model = ContestModel

    def find(self, **kwargs):
        return Base.find(self, model=self.contest_model, **kwargs)

    def create(self, **kwargs):
        contest = self.init(model=self.contest_model, **kwargs)
        _ = self.notify(topic='contests', value={'uuid': str(contest.uuid)}, key='contest_created')
        return self.save(instance=contest)

    def update(self, uuid, **kwargs):
        contests = self.find(uuid=uuid)
        if not contests.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=contests.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        notification = f'contest_{kwargs["status"]}' if kwargs.get('status') and instance.status != kwargs.get(
            'status') else None
        contest = self.assign_attr(instance=instance, attr=kwargs)
        if notification:
            _ = self.notify(topic='contests', value={'uuid': str(contest.uuid)}, key=notification)
        return self.save(instance=contest)

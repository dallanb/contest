import logging
from http import HTTPStatus

from .base import Base
from ..common import ParticipantStatusEnum, ContestStatusEnum
from ..decorators import contest_notification
from ..models import Contest as ContestModel, Participant as ParticipantModel


class Contest(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.contest_model = ContestModel
        self.participantModel = ParticipantModel

    def find(self, **kwargs):
        return Base.find(self, model=self.contest_model, **kwargs)

    @contest_notification(operation='create')
    def create(self, **kwargs):
        contest = self.init(model=self.contest_model, **kwargs)
        return self.save(instance=contest)

    def update(self, uuid, **kwargs):
        contests = self.find(uuid=uuid)
        if not contests.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=contests.items[0], **kwargs)

    @contest_notification(operation='update')
    def apply(self, instance, **kwargs):
        # if contest status is being updated we will trigger a notification
        contest = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=contest)

    # Check and update contest status if all participants associated with the contest have responded
    def check_contest_status(self, uuid):
        if ParticipantModel.query.filter_by(contest_uuid=uuid,
                                            status=ParticipantStatusEnum.pending.name).first() is None:
            contests = self.find(uuid=uuid)
            contest = contests.items[0]
            if contest.status == ContestStatusEnum.pending.name:
                self.apply(instance=contest, status=ContestStatusEnum.ready.name)

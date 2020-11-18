import logging
from http import HTTPStatus
from sqlalchemy import func

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
        status_counts = ParticipantModel.query.with_entities(ParticipantModel.status,
                                                             func.count(ParticipantModel.status)).filter_by(
            contest_uuid=uuid).group_by(ParticipantModel.status).all()
        counts = dict(status_counts)
        contests = self.find(uuid=uuid)
        contest = contests.items[0]

        if ContestStatusEnum[contest.status.name] == ContestStatusEnum['pending'] and not counts.get(
                ParticipantStatusEnum[contest.status.name], -1):
            self.apply(instance=contest, status=ContestStatusEnum.ready.name)
        elif ContestStatusEnum[contest.status.name] == ContestStatusEnum[
            'active'] and not counts.get(ParticipantStatusEnum[contest.status.name], -1):
            self.apply(instance=contest, status=ContestStatusEnum.completed.name)

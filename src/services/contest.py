import datetime
import logging
from http import HTTPStatus

from sqlalchemy import func

from .base import Base
from ..common import ParticipantStatusEnum, ContestStatusEnum
from ..decorators import contest_notification
from ..external import Course as CourseExternal
from ..models import Contest as ContestModel, Participant as ParticipantModel


class Contest(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.contest_model = ContestModel

    def find(self, **kwargs):
        return self._find(model=self.contest_model, **kwargs)

    def init(self, **kwargs):
        return self._init(model=self.contest_model, **kwargs)

    @contest_notification(operation='create')
    def create(self, **kwargs):
        contest = self._init(model=self.contest_model, **kwargs)
        return self._save(instance=contest)

    def update(self, uuid, **kwargs):
        contests = self.find(uuid=uuid)
        if not contests.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=contests.items[0], **kwargs)

    @contest_notification(operation='update')
    def apply(self, instance, **kwargs):
        # if contest status is being updated we will trigger a notification
        contest = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=contest)

    # Check and update contest status if all participants associated with the contest have responded
    def check_contest_status(self, uuid):
        status_counts = ParticipantModel.query.with_entities(ParticipantModel.status,
                                                             func.count(ParticipantModel.status)).filter_by(
            contest_uuid=uuid).group_by(ParticipantModel.status).all()
        counts = dict(status_counts)
        contests = self.find(uuid=uuid)
        contest = contests.items[0]

        if ContestStatusEnum[contest.status.name] == ContestStatusEnum['pending'] and not counts.get(
                ParticipantStatusEnum[contest.status.name]):
            self.apply(instance=contest, status=ContestStatusEnum.ready.name)
        elif ContestStatusEnum[contest.status.name] == ContestStatusEnum[
            'active'] and not counts.get(ParticipantStatusEnum[contest.status.name]):
            self.apply(instance=contest, status=ContestStatusEnum.completed.name)

    def fetch_location(self, uuid):
        hit = self.cache.get(uuid)
        if hit:
            return hit
        try:
            res = CourseExternal().fetch_course(uuid=uuid)
            location = res['data']['courses']
            self.cache.set(uuid, location, 3600)
            return location
        except TypeError:
            self.logger.error(f'fetch location failed for uuid: {uuid}')
            return None

    def find_by_start_time_range(self, month, year, **kwargs):
        query = self.db.clean_query(model=self.contest_model, **kwargs)
        min_start_time = datetime.datetime(year=year, month=month, day=1).timestamp() * 1000
        max_start_time = datetime.datetime(year=year, month=month + 1, day=1).timestamp() * 1000
        query = query.filter(self.contest_model.start_time > min_start_time,
                             self.contest_model.start_time < max_start_time)
        return self.db.run_query(query=query)

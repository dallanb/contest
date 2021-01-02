import logging
from http import HTTPStatus

from ..base import Base
from ..contest import Contest as ContestService
from ..participant import Participant as ParticipantService
from ...models import ContestMaterialized as MaterializedModel


class ContestMaterialized(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.contest_service = ContestService()
        self.participant_service = ParticipantService()
        self.materialized_model = MaterializedModel

    def find(self, **kwargs):
        return Base.find(self, model=self.materialized_model, **kwargs)

    def create(self, **kwargs):
        materialized_contest = self.init(model=self.materialized_model, **kwargs)
        return self.save(instance=materialized_contest)

    def update(self, uuid, **kwargs):
        materialized_contests = self.find(uuid=uuid)
        if not materialized_contests.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=materialized_contests.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        materialized_contest = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=materialized_contest)

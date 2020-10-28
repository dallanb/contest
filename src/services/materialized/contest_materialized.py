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

    def handle_event(self, key, data):
        if key == 'contest_created':
            contests = self.contest_service.find(uuid=data['uuid'])
            if contests.total:
                contest = contests.items[0]
                self.create(
                    uuid=contest.uuid,
                    name=contest.name,
                    status=contest.status.name,
                    participants={str(contest.owner_uuid): {}}
                )
        elif key == 'contest_updated':
            self.logger.info('contest updated')
        elif key == 'participant_active':
            participants = self.participant_service.find(uuid=data['participant_uuid'])
            if participants.total:
                contests = self.find(uuid=data['contest_uuid'])
                if contests.total:
                    contest = contests.items[0]
                    contest.participants[data['user_uuid']] = {}  # maybe fix this to conform to the rest of the code
                    self.db.save(instance=contest)
        elif key == 'avatar_created':
            contests = self.contest_service.find(uuid=data['contest_uuid'])
            if contests.total:
                contest = contests.items[0]
                self.update(
                    uuid=contest.uuid,
                    avatar=data['s3_filename']
                )

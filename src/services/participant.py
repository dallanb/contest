import concurrent.futures
import logging
from http import HTTPStatus

from .base import Base
from ..common import ParticipantStatusEnum
from ..decorators import participant_notification
from ..external import Member as MemberExternal
from ..models import Participant as ParticipantModel


class Participant(Base):

    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.participant_model = ParticipantModel

    def find(self, **kwargs):
        return Base.find(self, model=self.participant_model, **kwargs)

    @participant_notification(operation='create')
    def create(self, **kwargs):
        participant = self.init(model=self.participant_model, **kwargs)
        return self.save(instance=participant)

    def update(self, uuid, **kwargs):
        participants = self.find(uuid=uuid)
        if not participants.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=participants.items[0], **kwargs)

    @participant_notification(operation='update')
    def apply(self, instance, **kwargs):
        # if contest status is being updated we will trigger a notification
        _ = self._status_machine(instance.status.name, kwargs['status'])
        participant = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=participant)

    def _status_machine(self, prev_status, new_status):
        # cannot go from active to pending
        if ParticipantStatusEnum[prev_status] == ParticipantStatusEnum['active'] and ParticipantStatusEnum[
            new_status] == ParticipantStatusEnum['pending']:
            self.error(code=HTTPStatus.BAD_REQUEST)
        return True

    def fetch_member_user(self, user_uuid, league_uuid):
        hit = self.cache.get(f'{user_uuid}_{league_uuid}')
        if hit:
            return hit
        res = MemberExternal().fetch_member_user(uuid=user_uuid, params={'league_uuid': league_uuid})
        member = res['data']['members']
        self.cache.set(f'{user_uuid}_{league_uuid}', member, 3600)
        return member

    # possibly turn this into a decorator (the caching part)
    def fetch_member(self, uuid):
        hit = self.cache.get(uuid)
        if hit:
            return hit
        res = MemberExternal().fetch_member(uuid=uuid)
        self.logger.info(res)
        self.logger.info(uuid)
        member = res['data']['members']
        self.cache.set(uuid, member, 3600)
        return member

    def fetch_member_batch(self, uuids):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.fetch_member, uuids)
        return

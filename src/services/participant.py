import logging
from http import HTTPStatus

from .base import Base
from .. import cache
from ..models import Participant as ParticipantModel
from ..common import ParticipantStatusEnum
from ..decorators import participant_notification
from ..external import Account as AccountExternal


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

    @staticmethod
    @cache.memoize(300)
    def fetch_account(uuid):
        res = AccountExternal().fetch_account(uuid=uuid)
        return res['data']['membership']

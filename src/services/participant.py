import logging
from http import HTTPStatus

from .base import Base
from ..models import Participant as ParticipantModel


class Participant(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.participant_model = ParticipantModel

    def find(self, **kwargs):
        return Base.find(self, model=self.participant_model, **kwargs)

    def create(self, **kwargs):
        participant = self.init(model=self.participant_model, **kwargs)
        return self.save(instance=participant)

    def update(self, uuid, **kwargs):
        participants = self.find(uuid=uuid)
        if not participants.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=participants.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        participant = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=participant)

    # used to create a participant for self
    def create_self(self, **kwargs):
        return self.create(**kwargs)

    # used to create a participant for some user other than self
    def create_other(self, **kwargs):
        participant = self.create(**kwargs)
        user_uuid = kwargs.get('user_uuid')
        contest = kwargs.get('contest')
        self.notify(topic='contests',
                    value={'contest_uuid': str(contest.uuid), 'participant_uuid': str(participant.uuid),
                           'user_uuid': str(user_uuid)},
                    key='participant_invited')  # possibly add a message that can be displayed as the notification
        return participant

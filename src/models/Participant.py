from sqlalchemy_utils import UUIDType
from .. import db
from ..common import ParticipantStatusEnum
from .mixins import BaseMixin


class Participant(db.Model, BaseMixin):
    user_uuid = db.Column(UUIDType(binary=False), nullable=False)

    # FK
    contest_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('contest.uuid'), nullable=False)
    status = db.Column(db.Enum(ParticipantStatusEnum), db.ForeignKey('participant_status.name'), nullable=False)

    # Relationship
    contest = db.relationship("Contest", back_populates="participants", lazy="noload")
    participant_status = db.relationship("ParticipantStatus")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Participant.register()

from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db
from ..common import ParticipantStatusEnum


class Participant(db.Model, BaseMixin):
    # Constraints
    __table_args__ = (db.UniqueConstraint('member_uuid', 'contest_uuid', name='member_contest'),)

    member_uuid = db.Column(UUIDType(binary=False))

    # FK
    contest_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('contest.uuid'), nullable=False)
    status = db.Column(db.Enum(ParticipantStatusEnum), db.ForeignKey('participant_status.name'), nullable=False)

    # Relationship
    contest = db.relationship("Contest", back_populates="participants")
    participant_status = db.relationship("ParticipantStatus")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Participant.register()

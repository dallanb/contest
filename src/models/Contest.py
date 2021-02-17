from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db
from ..common import ContestStatusEnum


class Contest(db.Model, BaseMixin):
    # this is a user_uuid not a member_uuid for notification purposes
    owner_uuid = db.Column(UUIDType(binary=False), nullable=False)

    league_uuid = db.Column(UUIDType(binary=False), nullable=True)
    name = db.Column(db.String, nullable=False)
    start_time = db.Column(db.BigInteger, nullable=False)
    location_uuid = db.Column(UUIDType(binary=False), nullable=False)

    # FK
    status = db.Column(db.Enum(ContestStatusEnum), db.ForeignKey('contest_status.name'), nullable=False)
    avatar_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('avatar.uuid'), nullable=True)

    # Relationship
    contest_status = db.relationship("ContestStatus")
    avatar = db.relationship("Avatar", back_populates="contest")
    participants = db.relationship("Participant", back_populates="contest")
    sport = db.relationship("Sport", uselist=False, back_populates="contest", lazy="joined")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Contest.register()

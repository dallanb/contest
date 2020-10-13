from sqlalchemy_utils import UUIDType
from .. import db
from .mixins import BaseMixin
from ..common import ContestStatusEnum


class Contest(db.Model, BaseMixin):
    owner_uuid = db.Column(UUIDType(binary=False), nullable=False)
    name = db.Column(db.String, nullable=False)
    start_time = db.Column(db.BigInteger, nullable=False)

    # FK
    status = db.Column(db.Enum(ContestStatusEnum), db.ForeignKey('contest_status.name'), nullable=False)
    avatar_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('avatar.uuid'), nullable=True)

    # Relationship
    contest_status = db.relationship("ContestStatus")
    avatar = db.relationship("Avatar", back_populates="contest", lazy="noload")
    participants = db.relationship("Participant", back_populates="contest", lazy="noload")
    sport = db.relationship("Sport", uselist=False, back_populates="contest")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Contest.register()

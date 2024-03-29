from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db


class Sport(db.Model, BaseMixin):
    sport_uuid = db.Column(UUIDType(binary=False), nullable=False)

    # FK
    contest_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('contest.uuid'), nullable=False, unique=True)

    # Relationship
    contest = db.relationship("Contest", back_populates="sport", lazy="joined")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Sport.register()

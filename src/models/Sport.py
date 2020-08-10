from sqlalchemy_utils import UUIDType
from .. import db
from .mixins import BaseMixin


class Sport(db.Model, BaseMixin):
    sport_uuid = db.Column(UUIDType(binary=False), nullable=False)

    # FK
    contest_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('contest.uuid'), nullable=False)

    # Relationship
    contest = db.relationship("Contest")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Sport.register()

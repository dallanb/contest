from sqlalchemy_utils import UUIDType, generic_repr
from .. import db, ma
from .mixins import BaseMixin
from ..common import ContestStatusEnum


class Contest(db.Model, BaseMixin):
    owner_uuid = db.Column(UUIDType(binary=False), nullable=False)

    # FK
    status = db.Column(db.Enum(ContestStatusEnum), db.ForeignKey('contest_status.name'), nullable=False)

    # Relationship
    contest_status = db.relationship("ContestStatus")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Contest.register()

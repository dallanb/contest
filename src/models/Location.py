from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db


class Location(db.Model, BaseMixin):
    location_uuid = db.Column(UUIDType(binary=False), primary_key=True, unique=True, nullable=False)

    # Relationship
    contest = db.relationship("Contest", back_populates="location", uselist=False, lazy="noload")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Location.register()

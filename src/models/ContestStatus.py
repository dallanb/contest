from ..common import ContestStatusEnum
from .. import db
from .mixins import StatusMixin


class ContestStatus(db.Model, StatusMixin):
    name = db.Column(db.Enum(ContestStatusEnum), primary_key=True, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


ContestStatus.register()

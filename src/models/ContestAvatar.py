from .mixins import BaseMixin
from .. import db


class ContestAvatar(db.Model, BaseMixin):
    s3_filename = db.Column(db.String, nullable=False)
    filename = db.Column(db.String, nullable=False)

    # Relationship
    contest = db.relationship("Contest", back_populates="contest_avatar", uselist=False, lazy="noload")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


ContestAvatar.register()

from .schema import AvatarUpdatedSchema
from ..base import Base


class avatar_updated(Base):
    key = 'avatar_updated'
    schema = AvatarUpdatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, avatar):
        data = cls.schema.dump({'avatar': avatar})
        return avatar_updated(data=data)

from .schema import AvatarCreatedSchema
from ..base import Base


class avatar_created(Base):
    key = 'avatar_created'
    schema = AvatarCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, contest, avatar):
        data = cls.schema.dump({'contest': contest, 'avatar': avatar})
        return avatar_created(data=data)

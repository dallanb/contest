from .schema import AvatarDeletedSchema
from ..base import Base


class avatar_deleted(Base):
    key = 'avatar_deleted'
    schema = AvatarDeletedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, avatar):
        data = cls.schema.dump({'avatar': avatar})
        return avatar_deleted(data=data)

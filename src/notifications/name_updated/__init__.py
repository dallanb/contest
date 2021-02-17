from .schema import NameUpdatedSchema
from ..base import Base


class name_updated(Base):
    key = 'name_updated'
    schema = NameUpdatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, contest):
        data = cls.schema.dump({'contest': contest})
        return name_updated(data=data)

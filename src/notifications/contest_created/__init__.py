from .schema import ContestCreatedSchema
from ..base import Base


class contest_created(Base):
    key = 'contest_created'
    schema = ContestCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, contest):
        data = cls.schema.dump({'contest': contest})
        return contest_created(data=data)
